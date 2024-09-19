from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI_API")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

# When testing locally, we bypass the .env and load the variables manually
# mongo_uri = "mongodb://blink:theadventuresofblink@localhost:27017/hangman?authSource=admin"
# db_name = "hangman"
# collection_name = "phrases"

client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

@app.route('/add', methods=['POST'])
def add_item():

    data = request.get_json()

    # Validate that 'phrase' is provided
    if 'phrase' not in data:
        return jsonify({"error": "Missing required parameter 'phrase'"}), 400
    
    if 'hint' not in data:
        return jsonify({"error": "Missing required parameter 'hint'"}), 400

    new_item = {
        "phrase": data['phrase'],
        "hint": data['hint'],
        "last_used": None,  # Set to null initially since it hasn't been used yet
        "access_count": 0  # Start the counter at 0
    }

    collection.insert_one(new_item)
    return jsonify({"status": "Item added", "id": str(new_item['_id'])}), 201

@app.route('/random', methods=['GET'])
def get_random_item():
    try:
        # Use aggregate to get a random document
        random_item = list(collection.aggregate([{"$sample": {"size": 1}}]))
        
        if random_item:
            random_item = random_item[0]
            
            # Ensure _id is correctly handled as ObjectId
            record_id = random_item['_id']

            # Update the record with the current timestamp and increment the counter
            collection.update_one(
                {"_id": ObjectId(record_id)},
                {
                    "$set": {"last_used": datetime.now()},
                    "$inc": {"access_count": 1}
                }
            )

            # Return the updated document
            random_item['_id'] = str(random_item['_id'])
            random_item['last_used'] = datetime.now()
            random_item['access_count'] += 1
            return jsonify(random_item), 200

        return jsonify({"error": "No items found"}), 404
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)