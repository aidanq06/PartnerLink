import json
from pymongo import MongoClient

# RUN THIS FILE TO IMPORT 25 COMPANIES INTO THE PROGRAM

# MongoDB connection string
with open("./assets/mongodb.json", 'r') as file:
    data = json.load(file)
    conn_str = data['conn_str']

# Connect to MongoDB
client = MongoClient(conn_str)
db = client['partnerlink']
partners_col = db['partners']

# Path to the JSON file - replace 'path_to_json_file.json' with the actual path
json_file_path = './demo/companies_data.json'

# Open and read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Import data into MongoDB
result = partners_col.insert_many(data)

# Output the result
print(f"Inserted {len(result.inserted_ids)} documents into the collection.")
