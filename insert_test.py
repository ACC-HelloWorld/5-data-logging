import os
from pymongo import MongoClient
from my_secrets import MONGODB_URI

def test_insert_implementation():
    """Test if insert.py can successfully insert data"""
    # Setup
    client = MongoClient(MONGODB_URI)
    db = client.get_database()
    collection = db.get_collection('test_collection')
    
    course_id = os.environ["COURSE_ID"]
    
    # Count documents before insertion
    initial_count = collection.count_documents({"course_id": course_id})
    
    # Run insert.py (this would normally run on microcontroller)
    import insert
    
    # Count documents after insertion
    final_count = collection.count_documents({"course_id": course_id})
    
    # Verify results
    assert final_count > initial_count, "No new documents were inserted"
    
    # Verify document structure
    doc = collection.find_one({"course_id": course_id})
    assert "command" in doc, "Document missing 'command' field"
    assert "sensor_data" in doc, "Document missing 'sensor_data' field"
    assert "experiment_id" in doc, "Document missing 'experiment_id' field"
    assert "timestamp" in doc, "Document missing 'timestamp' field"
    
    # Verify sensor data structure
    assert all(f"ch{w}" in doc["sensor_data"] 
              for w in [410, 440, 470, 510, 550, 583, 620, 670]), \
              "Sensor data missing expected wavelength channels"
    
    # Cleanup
    collection.delete_many({"course_id": course_id})
    client.close()

if __name__ == "__main__":
    test_insert_implementation()
