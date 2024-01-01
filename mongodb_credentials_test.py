import os
from pymongo.mongo_client import MongoClient
import requests

course_id_key = "COURSE_ID"

# general
database_key = "DATABASE_NAME"
collection_key = "COLLECTION_NAME"
cluster_name_key = "CLUSTER_NAME"

# data API specific
data_api_key_key = "DATA_API_KEY"
endpoint_base_url_key = "ENDPOINT_BASE_URL"

# For PyMongo
connection_string_key = "CONNECTION_STRING"


def test_env_vars_exists():
    for env_var in [
        course_id_key,
        database_key,
        collection_key,
        cluster_name_key,
        data_api_key_key,
        endpoint_base_url_key,
    ]:
        assert (
            env_var in os.environ
        ), f"Environment variable {env_var} does not exist. See README for instructions"


def test_connection():
    # Create a new client and connect to the server
    connection_string = os.environ[connection_string_key]
    client = MongoClient(connection_string)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
        success = True
    except Exception as e:
        success = False
        print(e)

    assert success, f"""Could not connect to MongoDB using the following URI: {connection_string}. 
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


def test_data_api():
    endpoint_base_url = os.environ[endpoint_base_url_key]
    data_api_key = os.environ[data_api_key_key]
    cluster_name = os.environ[cluster_name_key]
    database_name = os.environ[database_key]
    collection_name = os.environ[collection_key]
    course_id = os.environ[course_id_key]

    document = {"course_id": course_id}

    endpoint_url = f"{endpoint_base_url}/action/insertOne"

    num_retries = 3
    for _ in range(num_retries):
        response = requests.post(
            endpoint_url,
            headers={"api-key": data_api_key},
            json={
                "dataSource": cluster_name,
                "database": database_name,
                "collection": collection_name,
                "document": document,
            },
        )

        print(
            f"sending {document} to {cluster_name}:{database_name}:{collection_name} via {endpoint_base_url}"
        )

        txt = str(response.text)
        status_code = response.status_code

        print(f"Response: ({status_code}), msg = {txt}")

        if status_code == 201:
            print("Added Successfully")
            break

        print("Retrying...")

    assert (
        status_code == 201
    ), f"Received status code {status_code} and message {txt}. Failed to add {document} to {cluster_name}:{database_name}:{collection_name} via {endpoint_base_url}."


if __name__ == "__main__":
    test_env_vars_exists()
    test_connection()
    test_data_api()
