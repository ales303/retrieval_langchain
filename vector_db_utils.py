import db_utils
import openai
import utils

from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from langchain.callbacks import get_openai_callback
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


def create_collection(db_dir, collection_name):
    '''collection to a vector DB is like a table to a SQL DB.
       This funtion deletes a collection if it exists already and recreates it.
       Use with caution'''
    EMBEDDING_ADA_02_SIZE= 1536 #OpenAI embedding size
    client = QdrantClient(path=f"{db_dir}/", prefer_grpc=True)
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=EMBEDDING_ADA_02_SIZE, distance=Distance.COSINE),
        )



def get_connection(profile_id):
    profile_info = utils.load_configs()
    
    #openai.api_key = profile_info[profile_id]["openai_key"]
    embedding = OpenAIEmbeddings(openai_api_key=profile_info[profile_id]["openai_key"])

    db_path = f'{profile_info[profile_id]["qdrant_db_path"]}/qdrant_{profile_id}/'
    client = QdrantClient(path=db_path)
    conn = Qdrant(client=client, collection_name="collection1", embeddings=embedding)
    return conn, client

def release_connection(conn, client):
    del conn #free up the...
    del client #... db lock


def insert_to_db(doc_id, profile_id, content, meta=None):
    '''Id : user Id
       profile_id: profile Id
       content: content of the document as plain text (otherwise it will be `garbage in garbage out`)
       collection: name of the collection in the vector DB

       insert the content into vector DB along with the meta data
    '''

    #split content
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 150
        )
    splits = text_splitter.split_text(content)
    n_splits = len(splits)
    
    profile_info = utils.load_configs() #read ingfo from profile_configs.json
    openai.api_key = profile_info[profile_id]["openai_key"]
    
    #insert splits
    conn, client = get_connection(profile_id)
    
    #construct meta data
    if meta == None: # only meta is doc id
        meta = {'doc_id': doc_id}
    else: #insert doc_id to existing meta dict
        if 'doc_id' in meta:
            raise ValueError('`doc_id` already in the metadata. This key is not allowed.')
        meta['doc_id'] = doc_id


    with get_openai_callback() as cb:
        idx = conn.add_texts(splits,metadatas=[meta]*n_splits)
    utils.log_cost(profile_id, cb.total_tokens, cb.total_cost)
    
    #update Vectors table
    db_utils.insert_vectors(profile_id, idx, doc_id) 
    release_connection(conn, client)
    return idx

def similarity_search(query, profile_id, fetch_k=20, k=4):
    conn, client = get_connection(profile_id)
    docs = conn.max_marginal_relevance_search(query, fetch_k=fetch_k, k=k)
    
    release_connection(conn, client)
    return docs
    
def delete_vectors(indices, profile_id):
    conn, client = get_connection(profile_id)
    client.delete("collection1", indices)
    release_connection(conn, client)

    
def question_answer(profile_id, query, chat_history):
    
    profile_info = utils.load_configs() #read ingfo from profile_configs.json
    openai_api_key = profile_info[profile_id]["openai_key"]
    llm_name = profile_info[profile_id]["openai_model"]

    conn, client = get_connection(profile_id)

    qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(model_name=llm_name, temperature=0, openai_api_key=openai_api_key),
        retriever=conn.as_retriever(),
        #return_source_documents=True, # If you want to see which splits of docs are used
        #return_generated_question=True, # If you want to see 
    )

    with get_openai_callback() as cb:
        result = qa({"question": query, "chat_history": chat_history})
    utils.log_cost(profile_id, cb.total_tokens, cb.total_cost)
    
    chat_history.extend([(query, result["answer"])])

    return result["answer"], chat_history