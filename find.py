import os

# TODO: Other imports here
...

course_id = os.environ["COURSE_ID"]

database_name = os.environ["DATABASE_NAME"]
collection_name = os.environ["COLLECTION_NAME"]

atlas_uri = os.environ["ATLAS_URI"]

# TODO: Extract all entries from the database
...

# TODO: Create a pandas DataFrame per instructions in README
...

# TODO: Set '_id' as index and save to CSV
# Hint: Use df.set_index("_id") and df.to_csv()
...

# TODO: Close the client
...
