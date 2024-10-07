# This modified version:
# - Removed all code related to direct MongoDB connections.
# - Updated the environment variable checks to only verify COURSE_ID, AWS_API_GATEWAY_URL, and AWS_API_KEY.
# - Renamed the test_data_api() function to test_aws_api() and updated its content to use AWS API Gateway.
# - Removed the test_connection() function since we no longer connect directly to MongoDB.
# 
# This version of the script will test the connection and data insertion functionality of the AWS API Gateway 
# instead of directly testing the MongoDB connection.
# 
# Please ensure that the correct AWS_API_GATEWAY_URL and AWS_API_KEY are set in my_secrets.py or as environment variables.


import os
import requests

course_id_key = "COURSE_ID"
aws_api_gateway_url_key = "AWS_API_GATEWAY_URL"
aws_api_key_key = "AWS_API_KEY"

def test_env_vars_exists():
    for env_var in [
        course_id_key,
        aws_api_gateway_url_key,
        aws_api_key_key,
    ]:
        assert (
            env_var in os.environ
        ), f"Environment variable {env_var} does not exist. See README for instructions"

def test_aws_api():
    aws_api_gateway_url = os.environ[aws_api_gateway_url_key]
    aws_api_key = os.environ[aws_api_key_key]
    course_id = os.environ[course_id_key]

    document = {"course_id": course_id, "test": "test"}

    headers = {
        "x-api-key": aws_api_key,
        "Content-Type": "application/json"
    }

    num_retries = 3
    for _ in range(num_retries):
        response = requests.post(
            aws_api_gateway_url,
            headers=headers,
            json=document
        )

        print(f"sending {document} to AWS API Gateway")

        txt = str(response.text)
        status_code = response.status_code

        print(f"Response: ({status_code}), msg = {txt}")

        if status_code == 200:
            print("Added Successfully")
            break

        print("Retrying...")

    assert (
        status_code == 200
    ), f"Received status code {status_code} and message {txt}. Failed to add {document} via AWS API Gateway."

if __name__ == "__main__":
    test_env_vars_exists()
    test_aws_api()