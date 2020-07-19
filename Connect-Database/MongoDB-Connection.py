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
now = datetime.now()

collections = db.list_collection_names()
print(collections)
if(len(collections) > 2):
    minDate = collections[0].split('_')[1]
    for i in range(1,len(collections)):
        if(collections[i].split('_')[1]<minDate):
            minDate = collections[i].split('_')[1]
    db.drop_collection('venue_'+minDate)
    collections = db.list_collection_names()
    print(collections)

venue = db['venue_'+now.strftime("%Y-%m-%d %H:%M:%S")]


for filename in os.listdir(directory):
    if filename.endswith('.json'):
       print("Seeding ", os.path.splitext(os.path.basename(filename))[0], "into DB")
       data =[]
       with open(directory+filename, encoding='utf-8') as write_file:
           json_data = json.load(write_file)
       venue.insert_many(json_data)

