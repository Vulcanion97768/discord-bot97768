import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://discord-bot:mensomemo123@cluster0.6t6qh.mongodb.net/pokemon?retryWrites=true&w=majority")


db = client["Pokemon"]
collection = db["83742340920"]

post = {"name": "pokemon", "lvl": 10}

collection.find().sort("name", pymongo.ASCENDING)
collection.insert_one({"_id":1, "name":"ninetales", "lvl":5})



