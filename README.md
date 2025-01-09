# Logging Data
Write entries to a MongoDB database using a microcontroller and read them back using a Python script on your computer.

## The assignment
This assignment consists of two parts:
1. Using a microcontroller to run experiments and upload data (`insert.py`)
2. Using your computer to retrieve and analyze the data (`find.py`)

## MongoDB Setup and GitHub Secrets

For this assignment, you will need to add the [GitHub repository secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) listed below both as GitHub Actions secrets and Codespaces secrets, so that both you and the autograding scripts can access them. Please also keep a backup copy of these secrets in a secure location.

**The secrets to be added to GitHub Actions and Codespaces are:**
| Variable Name | Description |
|--------------|-------------|
| `COURSE_ID`  | Your student identifier for the course |
| `MONGODB_URI`| Your MongoDB connection string |

**Note:** If you encounter issues adding secrets to Codespaces, please refer to the "Alternative Methods for Handling Secrets" section at the end of this document.

## Insert

Update [`insert.py`](./insert.py) to iteratively run color experiments and insert the data into your MongoDB database. You will need to:

1. Connect to MongoDB using the provided URI
2. Run each experiment in `payload_dicts` using the `run_color_experiment()` function
3. Insert the results into the database

The document structure should be of the form:
```python
{
"command": {"R": ..., "G": ..., "B": ...},
"sensor_data": {"ch410": ..., "ch440": ..., ..., "ch670": ...},
"experiment_id": "...",
"course_id": "...",
"timestamp": "..."
}
```


## Find

Update [`find.py`](./find.py) to read all records from the database that have your course ID stored within the `course_id` field. Then, convert the results into a pandas DataFrame and save the output into a CSV file called `results.csv`.

Since your documents are nested dictionaries, you will need to use the `pd.json_normalize` function to flatten the nested dictionaries into a pandas DataFrame. For convenience, you can also set the `_id` column as the index of the pandas DataFrame via `.set_index("_id")`. See the example below:

```python
import pandas as pd
data = [
{
"id": "id1",
"category1": {"item1": 1, "item2": 2, "item3": 3},
"category2": {"itemA": 10, "itemB": 20, "itemC": 30},
},
{
"id": "id2",
"category1": {"item1": 4, "item2": 5, "item3": 6},
"category2": {"itemA": 40, "itemB": 50, "itemC": 60},
},
]
df = pd.json_normalize(data).set_index("id")
print(list(df.columns))
['category1.item1', 'category1.item2', 'category1.item3', 'category2.itemA', 'category2.itemB', 'category2.itemC']
print(df)
```

## Testing

The autograding workflow will run several tests to verify your implementation:
1. MongoDB credentials test
2. MongoDB connection test
3. Data insertion test
4. Data retrieval test

Make sure all tests pass before submitting your assignment.