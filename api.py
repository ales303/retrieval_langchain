from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from typing import List, Optional
import db_utils
import vector_db_utils
import utils
import json


app = FastAPI()

@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...), 
                       profile_id: str='',
                       uploader_username: str='',
                       department: str='',
                       purpose: str='',
                       notes: str='',
                       batch_run_datetime: str='',
                       batch_run_id: int = 0,
                       url: str=''
                       ):
    id_list= [] 
    for file in files:

        if file.content_type not in ['text/plain']:
            raise HTTPException(status_code=415, detail="Only plain text is supported.")

        # update records in sql tables
        doc_id = db_utils.insert_record(
                            file.filename, 
                            profile_id,
                            uploader_username,
                            department, 
                            purpose, 
                            notes, 
                            url,
                            batch_run_datetime, 
                            batch_run_id) 
        id_list.append(doc_id)

        contents = await file.read()  # Read the contents of the file
        vector_db_utils.insert_to_db(doc_id, 
                                     profile_id, 
                                     contents.decode()) #insert docs to vector db
        
    return {"message": "Files uploaded successfully", "ids":id_list}


@app.get("/get_docs")
def get_docs(profile_id: str, 
             start_date: str = None, 
             end_date: str = None):
    
    doc_list = db_utils.get_rows(profile_id, start_date, end_date)

    return doc_list

@app.post("/vector_search")
def vector_search(profile_id:int, query: str ):
    
    docs = vector_db_utils.similarity_search(query, profile_id)
    result = []

    for doc in docs:
        result.append({'content': doc.page_content, 'metadata': doc.metadata})

    return result


@app.post("/delete_docs")
def delete_docs(ids: List[int], profile_id: str=''):

    try:
        db_utils.mark_as_deleted(ids, profile_id)

        #delete the vectors from the vector DB
        indices = db_utils.get_vector_indices(ids)
        vector_db_utils.delete_vectors(indices, profile_id)

        return {'message': 'Documents marked as deleted.'}
    except Exception as e:
        return {f'message': 'Failed operation {e}'}


@app.post("/chat")
def chat(profile_id:int, query: str = Body(...), chat_history: List[Optional[List[str]]] = Body(...)):

    chat_history = utils.to_list_of_tuples(chat_history)
    ans, chat_history = vector_db_utils.question_answer(profile_id, query, chat_history)

    return {'answer': ans, 'chat_history': json.dumps(chat_history)}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost')