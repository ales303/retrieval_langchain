import vector_db_utils
import argparse
import os


def main(db_dir, collection):
    # Check if the collection exists
    collection_path = db_dir+ '/collection/' + collection
    if os.path.exists(collection_path):
        # Collection already exists
        print("Collection already exists! Either use a different path or collection name or delete the collection manually.")
        exit()
    
    vector_db_utils.create_collection(db_dir, collection)
    print("Collection created:", collection_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Create Vector DB")

    parser.add_argument("--db_dir", type=str, help="directory where db is stored", default='qdrant_db')
    parser.add_argument("--collection", type=str, help="Collection name", required=True, default='collection1')
    args = parser.parse_args()

    main(args.db_dir, args.collection)

    