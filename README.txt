Prerequisites
-------------
1. Install Anaconda if not already installed
# Search google for "install anaconda"

2. In Anaconda terminal, run:
> conda create -n myenv python=3.10
> conda activate myenv

3. Install dependencies:

> pip install -r requirements.txt

4. Replace "XXX" with OpenAI API key in profile_configs.JSON, for your user.


How to setup the chatbot backend
--------------------------------

1. Add a user along with their sqlite and qdrant databases.
> python add_user_profile.py --profile_config_file profile_configs.json

For more options do: python add_user_profile.py -h

2. Seed the databases with some corpus
> python  seed_databases.py --profile_id 1 --corpus_path destwin_text_files

3. Run webapplication for APIs
> uvicorn api:app --port 8080 
This will start Uvicorn on http://127.0.0.1:8080
You can point your browser to see and test the APIs manually: http://127.0.0.1:8080/docs

4. How to use chat function? Please see the code.
a. Example code that connects to API
> python test_chat_api.py

b. without going through the API
> python test_chat.py


5. Close virtual environment
> conda deactivate

ISSUES:
1. Embeddings generator is not giving the cost and tokens.