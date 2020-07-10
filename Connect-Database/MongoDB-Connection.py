# A MongoDB Atlas DB cluster has been set up
from pymongo import MongoClient
import os

MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")

client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.get_database('CherryPickerDB')
records = db.RawDataCollection
print(records.count_documents({}))  # Should output 0
