from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Load environment variables
load_dotenv()

app = Flask(__name__)
# Allow requests from the default Vite frontend URL
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# --- Database Connection ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/user_db")
DB_NAME = MONGO_URI.split("/")[-1]
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
db = client["user_db"]
users_collection = db.users


# --- Helper Function ---
def serialize_doc(doc):
    """Converts a MongoDB doc to a JSON-serializable format."""
    doc["_id"] = str(doc["_id"])
    return doc


# --- API Endpoints ---


@app.route("/api/users", methods=["GET"])
def get_users():
    """Fetch all users."""
    users = [serialize_doc(user) for user in users_collection.find()]
    return jsonify(users)


@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Fetch a single user by ID."""
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return jsonify(serialize_doc(user))
    return jsonify({"error": "User not found"}), 404


@app.route("/api/users/<user_id>", methods=["PATCH"])
def update_user(user_id):
    """Partially update an existing user (no field constraints)."""
    data = request.json or {}

    try:
        object_id = ObjectId(user_id)
    except InvalidId:
        return jsonify({"error": "Invalid user ID format"}), 400

    result = users_collection.update_one({"_id": object_id}, {"$set": data})

    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    updated_user = users_collection.find_one({"_id": object_id})
    return jsonify(serialize_doc(updated_user))


@app.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user by ID."""
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 204


# ... (POST, PUT, DELETE routes are in the repository) ...

if __name__ == "__main__":
    app.run(debug=True, port=5000)
