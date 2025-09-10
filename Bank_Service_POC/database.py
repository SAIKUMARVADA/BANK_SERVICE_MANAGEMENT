from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb+srv://saikumarvada23:Saikumar143@resumestore.arpzpqu.mongodb.net/?retryWrites=true&w=majority&appName=Resumestore")

db = client["bank_service_poc"]

# Collections
accounts_collection = db["accounts"]
transactions_collection = db["transactions"]
loans_collection = db["loans"]