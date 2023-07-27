import json
from pymongo import MongoClient

def get_mongo_db():
    with open('config.json') as f:
        config = json.load(f)
    
    mongo_url = config['mongo_url']
    db_name = config['database_name']

    client = MongoClient(mongo_url)
    db = client[db_name]
    
    return db