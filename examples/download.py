import os
from datetime import datetime, timedelta
from pychmirad import ChmiRad

# Nastavení složky pro ukládání dat
download_dir = os.path.expanduser("~/chmi_data")  # Uloží data do ~/chmi_data
dataset_type = "maxz"  # Změňte na požadovaný typ dat

# Inicializace objektu ChmiRad
chmi_rad = ChmiRad(dataset_type=dataset_type, download_dir=download_dir)

# Nastavení časového intervalu
#latest_datetime = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
#start_datetime = latest_datetime - timedelta(minutes=60*5)

start_datetime = datetime(2025, 1, 7, 10, 0, 0)
latest_datetime = datetime(2025, 1, 7, 15, 0, 0)

# Stažení dat
chmi_rad.download_data_range(start_datetime, latest_datetime)

# Změna datasetu a stažení dalších dat
chmi_rad.set_dataset_type("pseudocappi2km")
chmi_rad.download_data_range(start_datetime, latest_datetime)

