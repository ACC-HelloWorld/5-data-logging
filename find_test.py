"""Test the find.py implementation for MongoDB data retrieval"""

import os
import pandas as pd
from pymongo import MongoClient
from my_secrets import MONGODB_URI

def test_find_implementation():
    """Test if find.py can successfully retrieve and format data"""
    # Setup test data
    client = MongoClient(MONGODB_URI)
    db = client.get_database()
    collection = db.get_collection('test_collection')
    
    course_id = os.environ["COURSE_ID"]
    
    # Insert test document
    test_doc = {
        "command": {"R": 255, "G": 0, "B": 0},
        "sensor_data": {
            "ch410": 25.5,
            "ch440": 51.0,
            "ch470": 76.5,
        },
        "experiment_id": "test123",
        "course_id": course_id
    }
    collection.insert_one(test_doc)
    
    # Run find.py (this will create results.csv)
    import find
    
    # Verify results
    df = pd.read_csv("results.csv", index_col="_id")
    assert not df.empty, "No data was retrieved"
    assert "command.R" in df.columns, "Nested data was not properly flattened"
    assert "sensor_data.ch410" in df.columns, "Sensor data was not properly flattened"
    
    # Cleanup
    collection.delete_many({"course_id": course_id})
    client.close()

if __name__ == "__main__":
    test_find_implementation()