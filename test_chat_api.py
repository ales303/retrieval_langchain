import requests
import json

BASE_URL = "http://localhost:8080/chat"  # Update with the correct base URL of your FastAPI app

def test_process_chat(query, history):
    params = {
        "profile_id": 2
            }
    payload = {
        "query": query,
        "chat_history": history
        }

    response = requests.post(BASE_URL, params=params, json=payload)

    assert response.status_code == 200
    return response.json()

if __name__ == '__main__':

    history = [] #always start with empty list for new session
    
    response = test_process_chat("what is Destwin?", history)
    #response JSON object have 2 keys: "answer" and "chat_history"
    # you need to pass chat_history in the current session

    print('ans:',response["answer"])
    history = response["chat_history"] # this is a string
    history = json.loads(history) #convert it to json object

    response = test_process_chat("what are those features?", history)
    print('ans:',response["answer"])


