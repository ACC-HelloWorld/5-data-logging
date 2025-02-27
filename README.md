# Logging Data
Write entries to a database using a microcontroller and read them back using a Python script.

## The assignment
The tests are failing right now because your MongoDB credentials have not been added as GitHub repository secrets and because the two scripts ([`insert.py`](./insert.py) and [`find.py`](./find.py)) are not yet implemented. Wherever you see `...` within the script requires you to write your own code.

## MongoDB Setup and GitHub Secrets

For this assignment, you will need to add the [GitHub repository secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) listed below both as GitHub Actions secrets and Codespaces secrets, so that both you and the autograding scripts can access them. Please also keep a backup copy of these secrets in a secure location.

**The secrets to be added to GitHub Actions and Codespaces are:**
| Variable Name         | Description                                                                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `COURSE_ID`           | Your student identifier for the course                                                                                                                 |
| `DATABASE_NAME`       | The name of your database within the cluster                                                                                                           |
| `COLLECTION_NAME`     | The name of the collection from your database                                                                                                          |
| `LAMBDA_FUNCTION_URL` | The Lambda Function URL that acts as an intermediate layer between the microcontroller and the orchestrator                                            |
| `ATLAS_URI`           | The MongoDB Atlas universal resource identifier (URI) for the Python orchestrator to connect to MongoDB (sometimes referred to as a connection string) |

While tedious, this approach is a one-time setup that simplifies the development and autograding process while adhering to security best practices. Your `COURSE_ID` can be accessed from the main course website by referencing the corresponding quiz response from the main course website. Instructions based on step 13a from [the Build Instructions manuscript](https://doi.org/10.1016/j.xpro.2023.102329) for each of the remaining secrets and instructions on how to add secrets are provided in the following sections.

### Account and Cluster Setup

First, [set up your MongoDB account](https://account.mongodb.com/account/register) and [create a free-tier M0 cluster](https://www.mongodb.com/docs/guides/atlas/cluster/). Choose a cluster name* such as `test-cluster` and take note of the name (`CLUSTER_NAME`).

<sub>*`CLUSTER_NAME` should be 23 characters or fewer and should not end with a hyphen `-` (based on [Atlas docs](https://www.mongodb.com/docs/manual/reference/limits/#mongodb-atlas-label-limits))</sub>

### Database User

Next, [create a database user](https://www.mongodb.com/docs/guides/atlas/db-user/) with read and write permissions and store this information in a secure location.

### Network Configuration

Add `0.0.0.0/0` to [the network configuration](https://www.mongodb.com/docs/guides/atlas/network-connections/) to allow access from anywhere.

### Database and Collection

Follow the `Creating a MongoDB Database with the Atlas UI` instructions within the [Create a Database guide](https://www.mongodb.com/basics/create-database). Take note of the database name (`DATABASE_NAME`) and collection name (`COLLECTION_NAME`) that you choose: for example, `test-db` and `test-collection`, respectively.

<!-- ![Creating the database and collection](create-db-collection.gif) -->

### Atlas URI

You will also need to copy the [MongoDB Atlas URI](https://www.mongodb.com/docs/guides/atlas/connection-string/) for your cluster. Refer to the video below. IMPORTANT: After copying the Atlas URI (connection string), you will need to manually populate `<password>` with your database user password before adding this as a GitHub secret. For example, if the copy-pasted Atlas URI is `mongodb+srv://sgbaird:<password>@test-cluster.ab123.mongodb.net/?retryWrites=true&w=majority` and your MongoDB password is `HGzZNsQ3vBLKrXXF`, then your `ATLAS_URI` would be `mongodb+srv://sgbaird:HGzZNsQ3vBLKrXXF@test-cluster.ab123.mongodb.net/?retryWrites=true&w=majority`.

![Finding MongoDB Atlas URI Cluster ID](./readme-images/mongodb-connect-uri.gif)

### AWS Lambda Function

NOTE: The instructions for this section are based on the [Lambda getting started guide](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html). There are more advanced ways to set up Lambda functions, but the following steps and level of complexity are tailored to our simple use-case.

First, [create an AWS account](https://portal.aws.amazon.com/billing/signup) (you will need a credit card, but the free tier should be sufficient). Next, you'll create a new Lambda function:

1. Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.
2. Choose **Create function**.
3. Select **Author from scratch**.
4. In the **Basic information** pane, for **Function name**, enter a name (e.g., `dataLogging`).
5. For **Runtime**, choose **Python 3.13**.
6. Click the dropdown for **Additional Configurations**
7. Check the **Enable function URL** box
8. Under **Auth type**, select **None**
9. Check the **Configure cross-origin resource sharing (CORS) box

Your settings should look like the following, with everything else left as default:

![AWS Lambda Function Configuration](./readme-images/aws-lambda-configuration.png)

10. Finally, click Create function.

Open and run the [Preparing the Python code and dependencies for AWS Lambda](https://colab.research.google.com/github/AccelerationConsortium/ac-microcourses/blob/main/docs/courses/hello-world/1.5.2-mongodb-aws-lambda-prep.ipynb) Colab notebook, which will allow you to save a `deployment.zip` file to your local machine. If you have trouble accessing or running the notebook, there is [a backup copy](https://github.com/AccelerationConsortium/ac-microcourses/blob/main/docs/courses/hello-world/deployment.zip) [[permalink](https://github.com/AccelerationConsortium/ac-microcourses/blob/7a648c7d149b955d1312013ad5c33090ea17c5a1/docs/courses/hello-world/deployment.zip)]. However, the notebook has the latest version and is instructive for how to use [Lambda functions with Python dependencies](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html).

Back on the Lambda function page, upload the `deployment.zip` file by clicking on the **Code** tab and selecting **Upload from** and **.zip** file, then choosing the `deployment.zip` file from your machine. Click **Save**.

In the code editor within `lambda_function.py`, you will add your `ATLAS_URI` as a [Lambda environment variable](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) (for a similar reason to why you added it as a secret to the GitHub repository). Navigate to the **Configuration** tab. Along the left sidebar, click **Environment variables**, then **Edit**.

![Edit env vars](./readme-images/edit-env-vars.png)

Add your Atlas URI as follows, ensuring that your database username and password are embedded correctly. Click **Save**.

![AWS Lambda Function Environment Variables](./readme-images/atlas-uri-env-var.png)

Note the **Function URL** from the top right of the page. This is your `LAMBDA_FUNCTION_URL`.

### Adding Secrets

The interfaces for adding secrets can be found via your GitHub repository's `Settings` tab under the `Security` section on the left sidebar. Click the corresponding dropdown item in the `Secrets and variables` dropdown menu. Alternatively, use the direct links to navigate to these pages, which will be of the form:
```html
https://github.com/ACC-HelloWorld/5-data-logging-<username>/settings/secrets/actions
```
and
```html
https://github.com/ACC-HelloWorld/5-data-logging-<username>/settings/secrets/codespaces
```
where `<username>` is replaced with your GitHub username. For example:
```html
https://github.com/ACC-HelloWorld/5-data-logging-sgbaird/settings/secrets/actions
```
and
```html
https://github.com/ACC-HelloWorld/5-data-logging-sgbaird/settings/secrets/codespaces
```

## Insert

Update [`insert.py`](./insert.py) based on [the tutorial example](https://ac-microcourses.readthedocs.io/en/latest/courses/hello-world/1.5-data-logging.html) to iteratively run 10 dummy color experiments and insert the data into your MongoDB database.

You are required to also log the original command (i.e., `R`, `G`, `B`) and `experiment_id` along with the sensor data. The dictionary should be of the form:

```python
{
    "command": {"R": ..., "G": ..., "B": ...},
    "sensor_data": {"ch410": ..., "ch440": ..., ..., "ch670": ...},
    "experiment_id": "...",
}
```

See the example below for how to combine the original payload dictionary with the new sensor data in MicroPython:

```python
payload_dict = {"command": {"R": 255, "G": 0, "B": 0}, "experiment_id": "abc123"}
sensor_data = {
    "ch410": 25,
    "ch440": 51,
    "ch470": 76,
    "ch510": 102,
    "ch550": 127,
    "ch583": 153,
    "ch620": 229,
    "ch670": 255,
}
results = payload_dict.copy()
results.update({"sensor_data": sensor_data})
# {'command': {'R': 255, 'G': 0, 'B': 0}, 'experiment_id': 'abc123', 'sensor_data': {'ch410': 25, 'ch440': 51, 'ch470': 76, 'ch510': 102, 'ch550': 127, 'ch583': 153, 'ch620': 229, 'ch670': 255}}
```
Note that Python's ["unpack" operator](https://chat.openai.com/share/0dd75ad3-f428-4439-a77b-cb3ccd9e4786) (`**`) is not supported in MicroPython on the Pico W, hence the copy-and-update approach above.

You will also need to fill out [`my_secrets.py`](my_secrets.py) (autogenerated by Codespaces) and upload it to your microcontroller. The file is created automatically when you create your codespace, but it is ignored by git (see [`.gitignore`](.gitignore)). You should not commit or push `my_secrets.py` to the GitHub repo.

When you are done implementing the script and have updated [`my_secrets.py`] on the microcontroller, upload the script and run it on your microcontroller.

## Find

Update [`find.py`](./find.py) based on [the tutorial example](https://ac-microcourses.readthedocs.io/en/latest/courses/hello-world/1.5.1-pymongo.html) to read all records from the database that have your course ID stored within the `course_id` field (see [PyMongo docs](https://pymongo.readthedocs.io/en/stable/tutorial.html)). Then, convert the results into a pandas DataFrame and save the output into a CSV file called `results.csv`.

Since your documents are nested dictionaries, you will need to use the `pd.json_normalize` function to flatten the nested dictionaries into a pandas DataFrame. For convenience, you can also set the `_id` column as the index of the pandas DataFrame via `.set_index("_id")`. See the example below:

```python
import pandas as pd

data = [
    {
        "_id": "id1",
        "category1": {"item1": 1, "item2": 2, "item3": 3},
        "category2": {"itemA": 10, "itemB": 20, "itemC": 30},
    },
    {
        "_id": "id2",
        "category1": {"item1": 4, "item2": 5, "item3": 6},
        "category2": {"itemA": 40, "itemB": 50, "itemC": 60},
    },
]

df = pd.json_normalize(data).set_index("_id")
print(list(df.columns))
# ['category1.item1', 'category1.item2', 'category1.item3', 'category2.itemA', 'category2.itemB', 'category2.itemC']
print(df)
#      category1.item1  category1.item2  category1.item3  category2.itemA  category2.itemB  category2.itemC
# _id                                                                                                      
# id1                1                2                3               10               20               30
# id2                4                5                6               40               50               60
```

NOTE: Committing and pushing `results.csv` is optional and will
not affect the autograding results.

## Setup command

See `postCreateCommand` from [`devcontainer.json`](.devcontainer/devcontainer.json).

## Run command
`pytest`

You can also use the "Testing" sidebar extension to easily run individual tests.

## Additional Resources
- [IP Access List docs](https://www.mongodb.com/docs/atlas/security/ip-access-list/#add-ip-access-list-entries) ("Atlas UI" instructions)
- [Create a Database guide](https://www.mongodb.com/basics/create-database).


Before, we mentioned that we strategically selected a minimal implementation of AWS Lambda functions. To elaborate, we chose to use a `.zip` file for the Python dependencies rather than an [AWS Lambda Layer](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html). The latter is a more advanced feature that allows you to share code across multiple functions. We chose to use the Lambda Function URL directly rather than an [API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html) because it is simpler and more direct for our use-case. We also chose to allow the Lambda Function URL to be accessible by any machine ([CORS](https://docs.aws.amazon.com/lambda/latest/api/API_Cors.html)) without [authentication](https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html) (other than knowing the URL itself). Finally, we chose to add our `ATLAS_URI` as an environment variable within the Lambda function rather than using [AWS Secrets Manager secrets in AWS Lambda functions](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html). The goal of this assignment is not to make you an expert at AWS Lambda, but rather to enable you to send data from your microcontroller directly to a database without overcomplicating things. If your usage of AWS Lambda grows, you may want to consider these more advanced features.

For some additional resources related to AWS Lambda:

- [AWS Lambda guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Best practices for working with AWS Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
