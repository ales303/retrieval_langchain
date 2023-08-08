import db_utils
import vector_db_utils
import create_sqlite_db
import create_qdrant_db
import add_user_profile

def test_sql_table(doc_id, PROFILE_ID, FILE_NAME):
    conn = db_utils.get_connection(PROFILE_ID)
    query = f"SELECT * FROM Documents WHERE id = {doc_id}"
    cursor = conn.cursor()
    cursor.execute(query)
        
    # Fetch the result
    result = cursor.fetchone()
    assert result[1] == FILE_NAME
    assert result[2] == PROFILE_ID

    print('SQLite test: OK')


def cleanup_sql_table(doc_id, PROFILE_ID):
    # Connect to the SQLite database
    conn = db_utils.get_connection(PROFILE_ID)
    cursor = conn.cursor()

    # Execute the DELETE query with the provided id
    query = f"DELETE FROM Documents WHERE Id = {doc_id}"
    cursor.execute(query)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

def test_qdrant_collection(docs, doc_id, PROFILE_ID):
    docs = vector_db_utils.similarity_search('test', PROFILE_ID, doc_id)
    assert docs # is there a record?
    assert docs[0].metadata['id'] == doc_id
    
    print('Qdrant test: OK')

def cleanup_qdrant(ids, PROFILE_ID):
    vector_db_utils.delete_vectors(ids, PROFILE_ID)


# Begin tests
#____________

PROFILE_ID = 666 #test user
uid= PROFILE_ID
qdrant_db_path = f"qdrant_databases/qdrant_{uid}"
sqlite_db_path = 'sqlite_databases'
profile_config_file = 'profile_configs.json'
#create user
uid = add_user_profile.add_user('xxx',
             'yyy',
             'xxx',
             '',
             '',
             '',
             'qdrant_databases',
             sqlite_db_path,
             profile_config_file,
             PROFILE_ID)

#create new sqlite db for test user
create_sqlite_db.main(sqlite_db_path, f'documents_{uid}.db')

#create new qdrant for test user
create_qdrant_db.main(qdrant_db_path, "collection1")

FILE_NAME = 'test_666.txt'
doc_id = db_utils.insert_record(
                            FILE_NAME, #filename
                            PROFILE_ID, #profile id
                            'tester', #uploader_username
                            'testing', #department
                            'test', #purpose
                            '', #notes
                            '', #url
                            '', #batch_run_datetime defaulted to now 
                            666, #batch_run_id
                            ) 

test_sql_table(doc_id, PROFILE_ID, FILE_NAME)


TEXT = 'TEST TEXT'
ids = vector_db_utils.insert_to_db(doc_id, PROFILE_ID, TEXT) #insert docs to vector db

test_qdrant_collection(ids, doc_id, PROFILE_ID)

cleanup_sql_table(doc_id,PROFILE_ID)
cleanup_qdrant(ids, PROFILE_ID)