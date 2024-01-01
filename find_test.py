import os
import pandas as pd
from pathlib import Path
from insert_test import results_check

n_decimals = 4

check_df = pd.json_normalize(results_check).round(n_decimals)


def test_find():
    # Test that a pandas object and CSV file are present

    # execute find.py
    namespace = {}
    script_name = "find.py"
    script_content = open(script_name).read()

    # delete results.csv if it exists
    Path("results.csv").unlink(missing_ok=True)

    exec(script_content, namespace)
    my_vars = list(namespace.values())

    # find the pandas df
    dfs = [var for var in my_vars if isinstance(var, pd.DataFrame)]

    # assert only one
    assert len(dfs) == 1, (
        f"Expected exactly 1 pandas DataFrame object, but found {len(dfs)}.\n"
        "Please ensure that your script produces exactly one DataFrame."
    )

    df = dfs[0]

    # Select only the columns of df that are present in check_df, round, and drop duplicates
    df_selected = df[check_df.columns].round(n_decimals).drop_duplicates()

    # Merge check_df with df_selected on common columns
    merged_df = pd.merge(check_df, df_selected, how="left", indicator=True)

    # Check that all rows in check_df have a match in df_selected
    df_matches = merged_df["_merge"] == "both"
    assert df_matches.all(), (
        "Not all rows in the expected DataFrame have a match in the actual DataFrame.\n"
        f"Expected DataFrame:\n{check_df.to_string()}\n"
        f"Actual DataFrame:\n{df_selected.to_string()}\n"
        f"Matches:\n{df_matches}"
    )

    # assert the CSV file exists
    csv_file = "results.csv"
    assert os.path.exists(csv_file), (
        f"Expected the file '{csv_file}' to exist, but it does not.\n"
        "Please ensure that your script writes the output to 'results.csv'."
    )

    csv_df = pd.read_csv(csv_file)  # assert that the CSV file is valid

    # Select only the columns of df that are present in check_df
    csv_df_selected = csv_df[check_df.columns].round(n_decimals).drop_duplicates()

    # Merge check_df with csv_df_selected on common columns
    merged_csv_df = pd.merge(check_df, csv_df_selected, how="left", indicator=True)

    # Check that all rows in check_df have a match in csv_df_selected
    csv_df_matches = merged_csv_df["_merge"] == "both"
    assert csv_df_matches.all(), (
        "Not all rows in the expected DataFrame have a match in the DataFrame from 'results.csv'.\n"
        f"Expected DataFrame:\n{check_df.to_string()}\n"
        f"DataFrame from 'results.csv':\n{csv_df_selected.to_string()}\n"
        f"Matches:\n{csv_df_matches}"
    )


if __name__ == "__main__":
    test_find()
