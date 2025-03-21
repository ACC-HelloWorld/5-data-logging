# This file needs to be run on your microcontroller
from netman import connectWiFi

from my_secrets import (
    SSID,
    PASSWORD,
    DATABASE_NAME,
    COLLECTION_NAME,
    COURSE_ID,
    LAMBDA_FUNCTION_URL,
)

# TODO: other imports here
...

# Connect to WiFi
connectWiFi(SSID, PASSWORD, country="US")


# Dummy function for running a color experiment
def run_color_experiment(R, G, B):
    """Simulate color sensor readings"""
    wavelengths = [410, 440, 470, 510, 550, 583, 620, 670]
    rw = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 1.0]
    gw = [0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.4, 0.2]
    bw = [0.9, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0]
    sensor_data = {
        f"ch{wavelength}": rw[i] * R + gw[i] * G + bw[i] * B
        for i, wavelength in enumerate(wavelengths)
    }
    return sensor_data


# NOTE: Even though experiment_id is hard-coded here, pretend that it was
# auto-generated by the "orchestrator" using Python: `secrets.token_hex(4)`
# See https://docs.python.org/3/library/secrets.html for more info.
# There is no built-in secrets module in MicroPython, so we prefer to call the
# microcontroller file with our credentials `my_secrets.py` instead of
# `secrets.py` to avoid confusion.
# fmt: off
documents = [
    {"command": {"R": 11, "G": 218, "B": 81}, "experiment_id": "dacc788d"},  # Malachite
    {
        "command": {"R": 127, "G": 255, "B": 212},
        "experiment_id": "ca236d4e",
    },  # Aquamarine
    {"command": {"R": 80, "G": 200, "B": 120}, "experiment_id": "bad820bb"},  # Emerald
    {"command": {"R": 115, "G": 106, "B": 255}, "experiment_id": "c15bae67"},  # Tanzanite
    {"command": {"R": 171, "G": 173, "B": 72}, "experiment_id": "673e6846"},  # Peridot
    {"command": {"R": 0, "G": 163, "B": 108}, "experiment_id": "32d35040"},  # Jade
    {"command": {"R": 21, "G": 176, "B": 26}, "experiment_id": "f998b465"},  # Tsavorite
    {"command": {"R": 38, "G": 97, "B": 156}, "experiment_id": "e0ad387b"},  # Lapis Lazuli
    {"command": {"R": 0, "G": 0, "B": 255}, "experiment_id": "69dca791"},  # Topaz
    {"command": {"R": 225, "G": 44, "B": 44}, "experiment_id": "39d832df"},  # Rhodolite
]
# fmt: on

# TODO: for each of the commands above, run the corresponding dummy color
# experiment and upload a document containing your course ID (use `course_id` as
# the key), the original command, the experiment ID, and the sensor data to your
# MongoDB collection. The dictionary should be of the form:
# {
#     "command": {"R": ..., "G": ..., "B": ...},
#     "sensor_data": {"ch410": ..., "ch440": ..., ..., "ch670": ...},
#     "experiment_id": "...",
# }
...
