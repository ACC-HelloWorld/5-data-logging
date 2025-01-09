# This file needs to be run on your microcontroller
from netman import connectWiFi
import urequests
import ujson
from my_secrets import (
    SSID,
    PASSWORD,
    MONGODB_URI,
    COURSE_ID
)

# Connect to WiFi
connectWiFi(SSID, PASSWORD, country="US")

def run_color_experiment(R, G, B):
    """Simulate color sensor readings"""
    wavelengths = [410, 440, 470, 510, 550, 583, 620, 670]
    rw = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.9, 1.0]
    gw = [0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.4, 0.2]
    bw = [0.9, 1.0, 0.8, 0.6, 0.4, 0.2, 0.1, 0.0]
    
    return {
        f"ch{wavelength}": rw[i] * R + gw[i] * G + bw[i] * B
        for i, wavelength in enumerate(wavelengths)
    }

# Pre-defined experiments
payload_dicts = [
    {"command": {"R": 11, "G": 218, "B": 81}, "experiment_id": "dacc788d"},  # Malachite
    {"command": {"R": 127, "G": 255, "B": 212}, "experiment_id": "ca236d4e"},  # Aquamarine
    {"command": {"R": 80, "G": 200, "B": 120}, "experiment_id": "bad820bb"},  # Emerald
]

# TODO: Create MongoDB client and verify connection
# Hint: Use urequests to connect to MongoDB
...

# TODO: For each experiment in payload_dicts:
# 1. Run the experiment using run_color_experiment()
# 2. Create a document with command, sensor_data, experiment_id, and course_id
# 3. Send document to MongoDB using urequests.post()
...