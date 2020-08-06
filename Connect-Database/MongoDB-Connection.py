# A MongoDB Atlas DB cluster has been set up
from pymongo import MongoClient
from datetime import datetime
import pytz
import os
import json

SGT = pytz.timezone('Asia/Singapore')

directory = './Data/'
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
print("connecting to mongoDB")
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.get_database('CherryPickerDB')

db.drop_collection('venues')
venue = db['venues']
now = datetime.now()
now_in_singapore = now.astimezone(SGT).strftime("%Y-%m-%d %H:%M:%S")

# load data to mongo
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        print("Seeding ", os.path.splitext(
            os.path.basename(filename))[0], "into DB")
        data = []
        with open(directory+filename, encoding='utf-8') as write_file:
            json_data = json.load(write_file)
            # add in updateOn attribute into each of the venue object
            for data in json_data:
                data["updateOn"] = now_in_singapore
                print(data)
                
        venue.insert_many(json_data)
