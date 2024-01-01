import os

# TODO: Other imports here
...

course_id = os.environ["COURSE_ID"]

cluster_name = os.environ["CLUSTER_NAME"]
database_name = os.environ["DATABASE_NAME"]
collection_name = os.environ["COLLECTION_NAME"]

connection_string = os.environ["CONNECTION_STRING"]

# TODO: Extract all entries from the database
...

# TODO: Create a flattened pandas DataFrame (see README)
...

# TODO: Export the dataframe to results.csv file
...

# TODO: Close the client
...
