from langchain.document_loaders import TextLoader
from glob import glob
import argparse
import os

import db_utils
import vector_db_utils


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Seed the databases with plain text docs")
    parser.add_argument("--profile_id", type=int, help="Profile Id", default=1, required=True)
    parser.add_argument("--corpus_path", type=str, help="Path to the plain text corpus files", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.corpus_path):
        print('Corpus path nor found')
        exit()

    for f in glob(args.corpus_path+'/*.txt')[:10]:
        print('processing', f)
        doc = TextLoader(f,encoding='utf-8').load()
        text = doc[0].page_content
        
        #insert to sql db
        
        doc_id = db_utils.insert_record(
                            f, #filename
                            args.profile_id, #profile id
                            'seeder', #uploader_username
                            'seed', #department
                            'seed', #purpose
                            '', #notes
                            '', #url
                            '', #batch_run_datetime defaulted to now 
                            0, #batch_run_id
                            ) 
        #example metadata
        meta_data = {'source': 'https://support.destwin.com/dokuwiki/doku.php', 'key2': 3.1415}

        vector_db_utils.insert_to_db(doc_id, args.profile_id, text, meta=meta_data) #insert docs to vector db
        
        
    