import sqlite3
from datetime import datetime
import utils

def get_connection(profile_id):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """

    profile_info = utils.load_configs()
    db_file = f'{profile_info[profile_id]["sqlite_db_path"]}/documents_{profile_id}.db'

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print("error: can't open file", db_file)
        exit()
        return None

    

    

def insert_record(document_name,
                  profile_id, 
                  uploader_username, 
                  department, 
                  purpose, 
                  notes, 
                  url,
                  batch_run_datetime, 
                  batch_run_id):

    conn = get_connection(profile_id)
    cursor = conn.cursor()
    uploadtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    #TODO change with proper value later
    batch_run_datetime = uploadtime

    # Construct the INSERT query with placeholders for the values
    query = """INSERT INTO Documents (Document_name, 
                                       Profile_id, 
                                       Uploader_username, 
                                       timestamp, 
                                       Department, 
                                       Purpose,
                                       Notes, 
                                       Url, 
                                       batch_run_datetime, 
                                       batch_run_id, 
                                       mark_deleted)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    # Define the values to be inserted into the table
    values = (document_name, 
              profile_id, 
              uploader_username, 
              uploadtime, 
              department, 
              purpose, 
              notes, 
              url,
              batch_run_datetime, 
              batch_run_id, 
              0)

    # Execute the INSERT query and retrieve the auto-incremented Id
    cursor.execute(query, values)
    inserted_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return inserted_id



def list_table(profile_id, table_name='Documents'):
    conn = get_connection(profile_id)
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve all rows from the specified table
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Print the column names
    columns = [description[0] for description in cursor.description]
    print(columns)

    # Print the rows
    for row in rows:
        print(row)

    conn.close()



def get_rows(profile_id: int, start_date: str = None, end_date: str = None) :
    conn = get_connection(profile_id)
    cursor = conn.cursor()

    # Construct the SELECT query with placeholders for optional conditions
    query = "SELECT * FROM Documents WHERE Profile_id = ? "
    conditions = [profile_id]

    if start_date is not None:
        query += " AND timestamp >= ?"
        conditions.append(start_date)

    if end_date is not None:
        query += " AND timestamp <= ?"
        conditions.append(end_date)

    # Execute the SELECT query and retrieve the rows
    cursor.execute(query, conditions)
    rows = cursor.fetchall()

        
    columns = ["Id", "Document_name", "Profile_id", 
               "Uploader_username", "timestamp", 
               "Department", "Purpose", "Notes",
               "Url", "batch_run_datetime", "batch_run_id", "mark_deleted"]

    # Prepare the rows as dictionaries with column names as keys
    result = []
    for row in rows:
        result.append(dict(zip(columns, row)))

    conn.close()
    return result


def mark_as_deleted(ids, profile_id):
    conn = get_connection(profile_id)
    cursor = conn.cursor()

    # Convert the list of IDs to a tuple for the SQL query
    id_tuple = tuple(ids)

    # Construct the UPDATE query
    query = f"UPDATE Documents SET mark_deleted = 1 WHERE Id IN {id_tuple}"

    # Execute the UPDATE query
    cursor.execute(query)

    conn.commit()
    conn.close()

def insert_vectors(profile_id, indices, doc_id):
    conn = get_connection(profile_id)
    cursor = conn.cursor()

    # Insert rows into the table
    for index in indices:
        query = f"INSERT INTO Vectors (Vector_id, Id) VALUES (?, ?)"
        values = (index, doc_id)
        cursor.execute(query, values)

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()


def get_vector_indices(profile_id, ids):
    conn = get_connection(profile_id)
    cursor = conn.cursor()

    # Fetch the indices for the given IDs
    query = "SELECT vector_id FROM Vectors WHERE ID IN ({})".format(','.join(['?'] * len(ids)))
    cursor.execute(query, ids)
    rows = cursor.fetchall()

    # Extract the indices from the fetched rows
    indices = [row[0] for row in rows]

    # Close the database connection
    conn.close()

    return indices