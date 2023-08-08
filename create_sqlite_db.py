import sqlite3
import argparse
import os

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")
    

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e :
        print('error', e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e :
        print('error', e)

def main(db_path, db_name):
    sql_create_Document = """ CREATE TABLE IF NOT EXISTS Documents (
                                    Id integer PRIMARY KEY,
                                    Document_name text,
                                    Profile_id integer,
                                    Uploader_username text,
                                    timestamp text,
                                    Department text,
                                    Purpose text,
                                    Notes text,
                                    Url text,
                                    batch_run_datetime text, 
                                    batch_run_id integer, 
                                    mark_deleted integer
                                ); """

    sql_create_Vector_ids = """CREATE TABLE IF NOT EXISTS Vectors (
                                    Vector_id string,
                                    Id integer
                                )"""
    
    create_directory_if_not_exists(db_path)
    full_db_path = f"{db_path}/{db_name}"
    conn = create_connection(full_db_path)
    create_table(conn, sql_create_Document)
    create_table(conn, sql_create_Vector_ids)
    


if __name__== '__main__':
    parser = argparse.ArgumentParser(description="Create new DB")
    
    parser.add_argument("--db_path", type=str, help="path for the db", default='sqlite_databases')
    parser.add_argument("--db_name", type=str, help="db name", required=True)
    args = parser.parse_args()


    main(args.db_path, args.db_name)    
