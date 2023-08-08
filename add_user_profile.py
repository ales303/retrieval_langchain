import json
import argparse, os
import create_sqlite_db
import create_qdrant_db

profile_template = {
        "id": 1,
        "openai_key": "XXX",
        "openai_embedding_model": "text-embedding-ada-002",
        "openai_model": "gpt-3.5-turbo",
        "hypertuning_to_use": {},
        "database_name": "",
        "database_user": "",
        "database_pass": "",
        "qdrant_db_path": "qdrant_databases",
        "sqlite_db_path": "sqlite_databases"
    }


def add_user(openai_key, 
             openai_embedding_model = 'gpt-3.5-turbo',
             openai_model = 'gpt-3.5-turbo',
             database_name = '', 
             database_user = '', 
             database_pass = '',
             qdrant_db_path = '',
             sqlite_db_path = '',
             profile_config_file = '',
             profile_id = None
             ):
    
    if os.path.exists(profile_config_file):
        with open(profile_config_file) as f:
            profile_config = json.load(f)
    
        if not profile_id:
            last_id = max(profile_config, key=lambda x: x["id"])["id"] #get last user id
            last_id += 1 #increment for the new user
        else:
            last_id = profile_id
    else:
        last_id = 1
        profile_config = []

    profile_template["id"] = last_id
    profile_template["openai_key"] = openai_key
    profile_template["openai_embedding_model"] = openai_embedding_model
    profile_template["openai_model"] = openai_model
    profile_template["database_name"] = database_name
    profile_template["database_user"] = database_user
    profile_template["database_pass"] = database_pass
    profile_template["qdrant_db_path"] = qdrant_db_path
    profile_template["sqlite_db_path"] = sqlite_db_path

    profile_config.append(profile_template) #add new user
    
    #write to file
    with open(profile_config_file, 'w') as f:
        json.dump(profile_config, f, indent=4)

    print(f'Added user id={last_id}')
    return last_id



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Add new user")
    
    parser.add_argument("--openai_key", type=str, help="OpenAI API key")
    parser.add_argument("--openai_embedding_model", type=str, help="OpenAI Embeddings Model", default = "text-embedding-ada-002")
    parser.add_argument("--openai_model", type=str, help="OpenAI Model", default = "gpt-3.5-turbo")
    parser.add_argument("--sqlite_db_path", type=str, help="path to Sqlite Database", default='sqlite_databases')
    parser.add_argument("--qdrant_db_path", type=str, help="path to Qdrant Database", default='qdrant_databases')
    parser.add_argument("--db_name", type=str, help="Connection to Database")
    parser.add_argument("--db_user", type=str, help="Database user name")
    parser.add_argument("--db_pass", type=str, help="Database user password")
    # -- keep collection fixed because each user gets their own db
    #parser.add_argument("--collection_name", type=str, help="vector_db_collection", default="collection1") 
    parser.add_argument("--profile_config_file", type=str, help="Path to profile config file", required=True)

    args = parser.parse_args()

    uid = add_user(args.openai_key,
             args.openai_embedding_model,
             args.openai_model,
             args.db_name,
             args.db_user,
             args.db_pass,
             args.qdrant_db_path,
             args.sqlite_db_path,
             args.profile_config_file)
    
    #create new sqlite db
    create_sqlite_db.main(args.sqlite_db_path, f'documents_{uid}.db')

    #create new qdrant
    create_qdrant_db.main(f"{args.qdrant_db_path}/qdrant_{uid}", "collection1")
