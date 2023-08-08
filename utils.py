import json

def load_configs():
    '''load the user configurations. Used in API backend'''
    with open('profile_configs.json') as f:
        userlist = json.load(f)
    
    id_info = {}

    for user in userlist:
        uid = user['id']
        id_info[uid] = {}
        id_info[uid]['openai_key'] = user['openai_key']
        id_info[uid]['openai_model'] = user['openai_model']
        id_info[uid]['qdrant_db_path'] = user['qdrant_db_path']
        id_info[uid]['sqlite_db_path'] = user['sqlite_db_path']

    return id_info


def log_cost(profile_id, num_tokens, cost):
    #log it somewhere
    print(f'\nCost for profile{profile_id}: ${cost}. Number of tokens: {num_tokens}\n\n\n')
    pass

def to_list_of_tuples(chat_history):
    result = []
    for entry in chat_history:
        result.append((entry[0], entry[1]))
    return result
