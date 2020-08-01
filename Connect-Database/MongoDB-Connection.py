# A MongoDB Atlas DB cluster has been set up
from pymongo import MongoClient
from datetime import datetime
import os
import json

directory = './Data/'
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
print("connecting to mongoDB")
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.get_database('CherryPickerDB')

venue = db['venues']

# load data to mongo
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        print("Seeding ", os.path.splitext(
            os.path.basename(filename))[0], "into DB")
        data = []
        with open(directory+filename, encoding='utf-8') as write_file:
            json_data = json.load(write_file)
        venue.insert_many(json_data)
