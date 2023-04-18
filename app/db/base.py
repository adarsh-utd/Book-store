import pymongo
import os

mongo_client = pymongo.MongoClient(os.environ['MONGODB_URL'])
db = mongo_client['book_store']

