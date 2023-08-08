import requests
import db_utils

def test_upload_files():
    url = "http://localhost:8080/upload_files"  # Replace with the actual URL of your FastAPI application

    files = [
        ("files", ("file1.txt", b'aaaaaa', "text/plain")),
        ("files", ("file2.txt", b'cccccc', "text/plain"))
    ]
    
    parameters = {
        "profile_id": "2",
        "uploader_username": "user123",
        "department": "IT",
        "purpose": "Archiving",
        "notes": "Some notes",
        "batch_run_datetime": "2023-07-06 12:00:00",
        "batch_run_id": 1,
        "url": "https://example.com/document.txt"
    }

    response = requests.post(url, files=files, params=parameters)

    assert response.status_code == 200
    response_data = response.json()
    assert  response_data['message'] ==  "Files uploaded successfully"

    return response_data['ids']

if __name__ == "__main__":
    test_upload_files()
    db_utils.list_table()