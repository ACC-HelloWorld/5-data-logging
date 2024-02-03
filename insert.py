# This file needs to be run on your microcontroller
from netman import connectWiFi

from my_secrets import (
    SSID,
    PASSWORD,
    COURSE_ID,
    DATA_API_KEY,
    ENDPOINT_BASE_URL,
    CLUSTER_NAME,
    DATABASE_NAME,
    COLLECTION_NAME,
)

# TODO: other imports here
...

connectWiFi(SSID, PASSWORD, country="US")


# Dummy function for running a color experiment
def run_color_experiment(R, G, B):
    """
    Run a color experiment with the specified RGB values.

    Parameters
    ----------
    R : int
        The red component of the color, between 0 and 255.
    G : int
        The green component of the color, between 0 and 255.
    B : int
        The blue component of the color, between 0 and 255.

    Returns
    -------
    dict
        A dictionary with the sensor data from the experiment.

    Examples
    --------
    >>> run_color_experiment(255, 0, 0)
    {'ch410': 25.5, 'ch440': 51.0, 'ch470': 76.5, 'ch510': 102.0, 'ch550': 127.5, 'ch583': 153.0, 'ch620': 229.5, 'ch670': 255.0} # noqa: E501
    """
    wavelengths = [410, 440, 470, 510, 550, 583, 620, 670]
    rw = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 1.0]
    gw = [0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.4, 0.2]
    bw = [0.9, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0]
    sensor_data = {
        f"ch{wavelength}": rw[i] * R + gw[i] * G + bw[i] * B
        for i, wavelength in enumerate(wavelengths)
    }
    return sensor_data


commands = [
    {"R": 11, "G": 218, "B": 81},  # Malachite
    {"R": 127, "G": 255, "B": 212},  # Aquamarine
    {"R": 80, "G": 200, "B": 120},  # Emerald
    {"R": 115, "G": 106, "B": 255},  # Tanzanite
    {"R": 171, "G": 173, "B": 72},  # Peridot
    {"R": 0, "G": 163, "B": 108},  # Jade
    {"R": 21, "G": 176, "B": 26},  # Tsavorite
    {"R": 38, "G": 97, "B": 156},  # Lapis Lazuli
    {"R": 0, "G": 0, "B": 255},  # Topaz
    {"R": 225, "G": 44, "B": 44},  # Rhodolite
]

# TODO: for each of the commands above, run the corresponding dummy color
# experiment and upload a document containing your course ID (use `course_id` as
# the key), the original command, the experiment ID, and the sensor data to your
# MongoDB collection. The dictionary should be of the form:
# {
#     "command": {"R": ..., "G": ..., "B": ...},
#     "sensor_data": {"ch410": ..., "ch440": ..., ..., "ch670": ...},
#     "experiment_id": "...",
# }
...  # IMPLEMENT
