import json
from dataclasses import dataclass, asdict
from datetime import datetime
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/user_db")

# --- FIX IS HERE ---
# 1. Connect to the MongoDB cluster using the full URI
client = pymongo.MongoClient(MONGO_URI)

# 2. Instead of parsing the URI, explicitly get the 'user_db' database from the client.
# This is the correct and robust way to do it.
db = client['user_db']
# --- END OF FIX ---

collection = db.users

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool
    created_ts: float
    updated_ts: float  # Added for CRUD functionality

def parse_and_import():
    """Parses data from udata.json and imports it into MongoDB."""
    
    # Clear the collection to avoid duplicates on re-runs
    collection.delete_many({})
    print("Cleared the 'users' collection.")

    with open('udata.json', 'r') as f:
        data = json.load(f)

    users_to_insert = []
    for u in data['users']:
        roles = []
        if u.get('is_user_admin'):
            roles.append('admin')
        if u.get('is_user_manager'):
            roles.append('manager')
        if u.get('is_user_tester'):
            roles.append('tester')

        # Convert created_at string to a Unix timestamp (float)
        created_timestamp = datetime.fromisoformat(u['created_at'].replace('Z', '+00:00')).timestamp()

        user_obj = User(
            username=u['user'],
            password=u['password'],
            roles=roles,
            preferences=UserPreferences(timezone=u['user_timezone']),
            active=u['is_user_active'],
            created_ts=created_timestamp,
            updated_ts=created_timestamp # Initially, updated_ts is same as created_ts
        )

        # Convert the dataclass object to a dictionary for MongoDB insertion
        user_dict = asdict(user_obj)
        users_to_insert.append(user_dict)

    if users_to_insert:
        collection.insert_many(users_to_insert)
        print(f"Successfully imported {len(users_to_insert)} users into the database.")
    else:
        print("No users to import.")

if __name__ == "__main__":
    parse_and_import()