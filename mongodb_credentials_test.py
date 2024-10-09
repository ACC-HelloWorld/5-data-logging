import os
from pymongo import MongoClient
from my_secrets import MONGODB_URI

def test_env_vars_exists():
    assert "COURSE_ID" in os.environ, "Environment variable COURSE_ID does not exist"

def test_mongodb_connection():
    client = MongoClient(MONGODB_URI)
    db = client.get_database()
    assert db.command("ping").get("ok") == 1, "Failed to connect to MongoDB"

if __name__ == "__main__":
    test_env_vars_exists()
    test_mongodb_connection()