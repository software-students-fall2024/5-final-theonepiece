import os
from pymongo import MongoClient

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(mongo_uri)
db = client.get_default_database()