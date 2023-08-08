import vector_db_utils
import requests
import json

def test_search_function(profile_id, query):
    query = "What is Destwin?"
    search_results = vector_db_utils.similarity_search(query, profile_id)
    print('Meta for query:', query)
    for doc in search_results:
        print(doc.metadata)



BASE_URL = "http://localhost:8000/vector_search"  # Update with the correct base URL of your FastAPI app

def test_search_api(profile_id, query):
    params = {
        "profile_id": profile_id,
        "query": query
        }
    
    response = requests.post(BASE_URL, params=params)

    #assert response.status_code == 200
    return response.json()



profile_id=1

#test the function in vector_db_utils
test_search_function(profile_id, 'What is Destwin')


#test the function via API
result = test_search_api(profile_id, 'What is Destwin')
print(json.dumps(result, indent=4))
