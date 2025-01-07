import requests
import h5py
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

class ChmiRad:
    DATA_TYPES = {
        # This is not fully correct.. Works only for some outputs

        "echotop": "hdf5/T_PANV23_C_OKPR_{}.hdf",
        "fct_maxz": "hdf5/T_PANV23_C_OKPR_{}.hdf",
        "fct_pseudocappi2km": "hdf5/T_PANV23_C_OKPR_{}.hdf",
        "maxz": "hdf5/T_PABV23_C_OKPR_{}.hdf",
        "merge1h": "hdf5/T_PASV23_C_OKPR_{}.hdf",
        "pseudocappi2km": "hdf5/T_PANV23_C_OKPR_{}.hdf",
        "maxz_png": "hdf5/T_PANV23_C_OKPR_{}.png",
        "echotop_png": "hdf5/T_PANV23_C_OKPR_{}.png",
        "merge1h_png": "png/T_PANV23_C_OKPR_{}.png"
    }
    
    def __init__(self, dataset_type='pseudocappi2km', download_dir='tmp'):
        self.dataset_type = dataset_type
        self.base_url_template = "http://opendata.chmi.cz/meteorology/weather/radar/composite/{}/{}"
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def set_dataset_type(self, dataset_type):
        if dataset_type not in self.DATA_TYPES:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
        self.dataset_type = dataset_type
        print(f"Dataset type set to: {dataset_type}")
    
    @staticmethod
    def format_datetime(dt):
        return dt.strftime('%Y%m%d%H%M%S')
    
    @staticmethod
    def round_down_to_nearest_five(dt):
        minute = (dt.minute // 5) * 5
        return dt.replace(minute=minute, second=0, microsecond=0)
    
    def get_file_url(self, data_datetime):
        formatted_datetime = self.format_datetime(data_datetime)
        filename = self.DATA_TYPES[self.dataset_type].format(formatted_datetime)
        return self.base_url_template.format(self.dataset_type, filename)
    
    def download_data(self, data_datetime):
        url = self.get_file_url(data_datetime)
        filename = os.path.join(self.download_dir, os.path.basename(url))
        
        if not os.path.exists(filename):
            print(f"Downloading data from: {url}")
            response = requests.get(url)
            
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print(f"File downloaded successfully, size: {len(response.content)} bytes")
            else:
                print(f"Failed to download file, status code: {response.status_code}")
                raise Exception("Failed to download data")
        else:
            print(f"File already exists: {filename}")
    
    def download_data_range(self, start_datetime, end_datetime, interval_minutes=10):
        start_datetime = self.round_down_to_nearest_five(start_datetime)
        end_datetime = self.round_down_to_nearest_five(end_datetime)
        
        current_datetime = start_datetime
        while current_datetime <= end_datetime:
            self.download_data(current_datetime)
            current_datetime += timedelta(minutes=interval_minutes)

# Example usage:
if __name__ == "__main__":
    dataset_type = "maxz"  # Change to desired dataset type
    download_dir = "data"  # Change to desired directory
    
    visualizer = ChmiRad(dataset_type=dataset_type, download_dir=download_dir)
    
    latest_datetime = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_datetime = latest_datetime - timedelta(minutes=60)
    visualizer.download_data_range(start_datetime, latest_datetime)
    
    # Change dataset type dynamically
    visualizer.set_dataset_type("maxz_png")
    visualizer.download_data(latest_datetime)
