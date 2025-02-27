import os
from pprint import pformat
import math
from pymongo.mongo_client import MongoClient

from mongodb_credentials_test import (
    course_id_key,
    database_key,
    collection_key,
    atlas_uri_key,
)

# fmt: off
documents = [
    {"command": {"R": 11, "G": 218, "B": 81}, "experiment_id": "dacc788d"},  # Malachite
    {"command": {"R": 127, "G": 255, "B": 212}, "experiment_id": "ca236d4e"},  # Aquamarine
    {"command": {"R": 80, "G": 200, "B": 120}, "experiment_id": "bad820bb"},  # Emerald
    {"command": {"R": 115, "G": 106, "B": 255}, "experiment_id": "c15bae67"},  # Tanzanite
    {"command": {"R": 171, "G": 173, "B": 72}, "experiment_id": "673e6846"},  # Peridot
    {"command": {"R": 0, "G": 163, "B": 108}, "experiment_id": "32d35040"},  # Jade
    {"command": {"R": 21, "G": 176, "B": 26}, "experiment_id": "f998b465"},  # Tsavorite
    {"command": {"R": 38, "G": 97, "B": 156}, "experiment_id": "e0ad387b"},  # Lapis Lazuli
    {"command": {"R": 0, "G": 0, "B": 255}, "experiment_id": "69dca791"},  # Topaz
    {"command": {"R": 225, "G": 44, "B": 44}, "experiment_id": "39d832df"},  # Rhodolite
]  # Hard-coded to match insert.py
# fmt: on


def flatten_dict(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    flattened = dict(items)
    if len(items) != len(set(k for k, v in items)):
        raise ValueError("Overlapping keys encountered.")
    return flattened


# Dummy function for running a color experiment
def run_color_experiment(R, G, B):
    # Hard-coded to match insert.py
    wavelengths = [410, 440, 470, 510, 550, 583, 620, 670]
    rw = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 1.0]
    gw = [0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.4, 0.2]
    bw = [0.9, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0]
    sensor_data = {
        f"ch{wavelength}": rw[i] * R + gw[i] * G + bw[i] * B
        for i, wavelength in enumerate(wavelengths)
    }
    return sensor_data


results_check = [
    {
        "command": document["command"],
        "sensor_data": run_color_experiment(**document["command"]),
        "experiment_id": document["experiment_id"],
    }
    for document in documents
]

flat_results_check = [flatten_dict(doc) for doc in results_check]


def test_documents_inserted():
    # add the course_id to each document
    for doc in results_check:
        doc["course_id"] = os.environ[course_id_key]

    # Create a new client and connect to the server
    atlas_uri = os.environ[atlas_uri_key]
    client = MongoClient(atlas_uri)

    # upload a test document
    db = client[os.environ[database_key]]
    collection = db[os.environ[collection_key]]

    # read the test document
    docs = list(collection.find({}))

    print(
        f"Found {len(docs)} documents in the {os.environ[collection_key]} collection."
    )

    flat_docs = [flatten_dict(doc) for doc in docs]

    # Check if each results_check document is present in docs, within tol for numerics
    for rc in flat_results_check:
        if not any(
            all(
                (
                    math.isclose(float(v), float(doc.get(k, None)), rel_tol=1e-4)
                    if isinstance(v, (float, int))
                    and isinstance(doc.get(k, None), (float, int))
                    else doc.get(k, None) == v
                )
                for k, v in rc.items()
            )
            for doc in flat_docs
        ):
            assert False, (
                "At least one document from results_check not found in docs:\n"
                f"{pformat(rc)}\n"
                "Refer back to the README for instructions. Then, check your script for missing "
                "or incorrect keys/values and try uploading a fresh copy "
                "of the dataset (no need to delete existing entries for this assignment)."
            )

    # close the connection
    client.close()


if __name__ == "__main__":
    test_documents_inserted()
