import os
import requests
import json
import pandas as pd
from my_secrets import AWS_API_GATEWAY_URL, AWS_API_KEY

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
headers = {"x-api-key": AWS_API_KEY}
params = {"course_id": course_id}  

response = requests.get(AWS_API_GATEWAY_URL, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    df = pd.json_normalize(data)
    df.set_index("_id", inplace=True) 
    df.to_csv("results.csv")
    print("Data successfully retrieved and saved to results.csv")
else:
    print(f"Error: {response.status_code}, {response.text}")
'''