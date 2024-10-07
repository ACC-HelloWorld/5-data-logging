import os
import pandas as pd
from pymongo import MongoClient
from my_secrets import MONGODB_URI

# TODO: Other imports here (if needed)
...

course_id = os.environ["COURSE_ID"]

# Note: We no longer need cluster_name, database_name, collection_name, and connection_string
# as we're using AWS API Gateway instead of direct MongoDB connection

# TODO: Extract all entries from the database using AWS API Gateway
# Hint: Use the requests library to make a GET request to the AWS API Gateway URL
# Don't forget to include the API key in the headers
...

# TODO: Create a flattened pandas DataFrame
# Hint: Use pd.json_normalize() to flatten the JSON data
...

# TODO: Export the dataframe to results.csv file
# Hint: Use the to_csv() method of the DataFrame
...

# Note: We no longer need to close the client as we're not directly connecting to MongoDB

# Example structure (you need to fill in the details):
'''
client = MongoClient(MONGODB_URI)
db = client.get_database()
collection = db['your_collection_name']

cursor = collection.find({"course_id": course_id})
data = list(cursor)

df = pd.json_normalize(data)
if '_id' in df.columns:
    df.set_index("_id", inplace=True)
df.to_csv("results.csv")
print("Data successfully retrieved and saved to results.csv")

client.close()
'''