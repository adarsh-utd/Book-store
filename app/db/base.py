import pymongo
import os

mongo_client = pymongo.MongoClient(os.environ['MONGODB_URL'])
db = mongo_client['book_store']

customers_collection = db['customers']
books_collection = db['books']