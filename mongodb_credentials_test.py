import os
from pymongo.mongo_client import MongoClient
import requests

course_id_key = "COURSE_ID"
database_key = "DATABASE_NAME"
collection_key = "COLLECTION_NAME"
atlas_uri_key = "ATLAS_URI"
lambda_function_url_key = "LAMBDA_FUNCTION_URL"


def test_env_vars_exists():
    for env_var in [
        course_id_key,
        database_key,
        collection_key,
        atlas_uri_key,
    ]:
        assert (
            env_var in os.environ
        ), f"Environment variable {env_var} does not exist. See README for instructions"


def test_connection():
    # Create a new client and connect to the server
    atlas_uri = os.environ[atlas_uri_key]
    client = MongoClient(atlas_uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
        success = True
    except Exception as e:
        success = False
        print(e)

    assert success, f"""Could not connect to MongoDB using the following URI: {atlas_uri}. 
    The URI should be of the format mongodb+srv://<username>:<password>@<cluster_name>.<cluster_id>.mongodb.net/?retryWrites=true&w=majority 
    where your cluster name and cluster ID can be found using the 'Connect' button interface on MongoDB Atlas. 
    For example, if your username is `test-user-find-only`, password is `HGzZNsQ3vBLKrXXF`, cluster name is `test-cluster`, and cluster ID is `c5jgpni`, 
    then your URI would be: mongodb+srv://sgbaird:HGzZNsQ3vBLKrXXF@test-cluster.c5jgpni.mongodb.net/?retryWrites=true&w=majority.
    Please check your environment variables and ensure your MongoDB database and collection are set up correctly."""

    # upload a test document
    db = client[os.environ[database_key]]
    collection = db[os.environ[collection_key]]
    test_document = {"test": "test"}
    collection.insert_one(test_document)
    print(f"Inserted a test document into the {os.environ[collection_key]} collection.")

    # read the test document
    test_document = collection.find_one(test_document)
    print(f"Found the test document in the {os.environ[collection_key]} collection.")

    # delete the test document
    collection.delete_one(test_document)
    print(
        f"Deleted the test document from the {os.environ[collection_key]} collection."
    )

    # close the connection
    client.close()


def test_lambda_function_url():
    database_name = os.environ[database_key]
    collection_name = os.environ[collection_key]
    course_id = os.environ[course_id_key]
    lambda_function_url = os.environ[lambda_function_url_key]

    document = {"course_id": course_id}

    payload = {
        "database": database_name,
        "collection": collection_name,
        "document": document,
    }

    response = requests.post(lambda_function_url, json=payload)

    assert (
        response.status_code == 200
    ), f"Received status code {response.status_code} and message {str(response.text)}. Failed to add {document} to {database_name}:{collection_name} via {lambda_function_url}."


if __name__ == "__main__":
    test_env_vars_exists()
    test_connection()
    test_lambda_function_url()
