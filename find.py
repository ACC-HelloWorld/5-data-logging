import os
import pandas as pd
from pymongo import MongoClient
from my_secrets import MONGODB_URI

# TODO: Other imports here (if needed)
...

course_id = os.environ["COURSE_ID"]

# TODO: Create MongoDB client and connect to database
# Hint: Use MongoClient(MONGODB_URI) and verify connection with ping
...

# TODO: Get database and collection
# Hint: Use client['database_name'] and db['collection_name']
...

# TODO: Query all documents with your course_id
# Hint: Use collection.find({"course_id": course_id})
...

# TODO: Create pandas DataFrame from results
# Hint: Use pd.DataFrame(results)
...

# TODO: Set '_id' as index and save to CSV
# Hint: Use df.set_index("_id") and df.to_csv()
...

# Don't forget to close the MongoDB connection!