import os
from datetime import datetime, timedelta
from pychmirad import ChmiRad


download_dir = os.path.expanduser("~/chmi_data")
dataset_type = "maxz"  # set reuired data type

# initialize ChmiRad class
chmi_rad = ChmiRad(dataset_type=dataset_type, download_dir=download_dir)

# Set timerange
start_datetime = datetime(2025, 1, 7, 8, 0, 0)
latest_datetime = datetime(2025, 1, 7, 21, 0, 0)

# Data download
chmi_rad.download_data_range(start_datetime, latest_datetime)

# new dataset
chmi_rad.set_dataset_type("maxz_png")
chmi_rad.download_data_range(start_datetime, latest_datetime)

chmi_rad.set_dataset_type("pseudocappi2km")
chmi_rad.download_data_range(start_datetime, latest_datetime)

chmi_rad.set_dataset_type("pseudocappi2km_png")
chmi_rad.download_data_range(start_datetime, latest_datetime)

