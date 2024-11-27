from pymongo import MongoClient
from bson.objectid import ObjectId

uri = "mongodb+srv://lezioni:itsfoggia@cluster0.u7ews.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

db = client['project_group1']

users_collection = db.users
plants_collection = db.plants
machinery_collection = db.machinery

def toString(obj_id: ObjectId) -> str:
    return str(obj_id)