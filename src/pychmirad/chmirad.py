import requests
import os
from datetime import datetime, timedelta
import datetime as dt

class ChmiRad:
    DATA_TYPES = {
        "maxz": {"filename": "T_PABV23_C_OKPR_{}.hdf", "date_format": "%Y%m%d%H%M%S", "path": "maxz/hdf5"},
        "pseudocappi2km": {"filename": "T_PANV23_C_OKPR_{}.hdf", "date_format": "%Y%m%d%H%M%S", "path": "pseudocappi2km/hdf5"},
        "pseudocappi2km_png": {"filename": "pacz2gmaps3.z_cappi020.{}.0.png", "date_format": "%Y%m%d.%H%M", "path": "pseudocappi2km/png"},
        "merge1h": {"filename": "T_PASV23_C_OKPR_{}.hdf", "date_format": "%Y%m%d%H%M%S", "path": "merge1h/hdf5"},
        "echotop": {"filename": "T_PADV23_C_OKPR_{}.hdf", "date_format": "%Y%m%d%H%M%S", "path": "echotop/hdf5"},
        "fct_maxz": {"filename": "T_PABV23_C_OKPR_{}_fctff.hdf", "date_format": "%Y%m%d%H%M%S", "path": "fct_maxz/hdf5"},
        "fct_pseudocappi2km": {"filename": "T_PANV23_C_OKPR_{}_fctff.hdf", "date_format": "%Y%m%d%H%M%S", "path": "fct_pseudocappi2km/hdf5"},
        "maxz_png": {"filename": "pacz2gmaps3.z_max3d.{}.0.png", "date_format": "%Y%m%d.%H%M", "path": "maxz/png/"},
        "merge1h_png": {"filename": "T_PASV23_C_OKPR_{}.png", "date_format": "%Y%m%d%H%M", "path": "merge1h/png"},
        "fct_maxz_tar": {"filename": "T_PABV23_C_OKPR_{}.ft60s10.tar", "date_format": "%Y%m%d.%H%M", "path": "fct_maxz/hdf5"},
        "fct_pseudocappi2km_tar": {"filename": "T_PANV23_C_OKPR_{}.ft60s10.tar", "date_format": "%Y%m%d.%H%M", "path": "fct_pseudocappi2km/hdf5"},
    }
    
    BASE_URL = "https://opendata.chmi.cz/meteorology/weather/radar/composite/{}/{}"

    def __init__(self, dataset_type='pseudocappi2km', download_dir='tmp'):
        if dataset_type not in self.DATA_TYPES:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
        self.dataset_type = dataset_type
        self.download_dir = os.path.expanduser(download_dir)
        os.makedirs(self.download_dir, exist_ok=True)

    def set_dataset_type(self, dataset_type):
        if dataset_type not in self.DATA_TYPES:
            raise ValueError(f"Unknown dataset type: {dataset_type}")
        self.dataset_type = dataset_type
        print(f"Dataset type set to: {dataset_type}")
    
    @classmethod
    def get_available_datasets(cls):
        """Returns a list of available dataset types."""
        return list(cls.DATA_TYPES.keys())
    
    def format_datetime(self, dt):
        return dt.strftime(self.DATA_TYPES[self.dataset_type]["date_format"])

    def get_file_url(self, data_datetime):
        formatted_datetime = self.format_datetime(data_datetime)
        filename = self.DATA_TYPES[self.dataset_type]["filename"].format(formatted_datetime)
        path = self.DATA_TYPES[self.dataset_type]["path"]
        return self.BASE_URL.format(path, filename), filename

    def download_data(self, data_datetime):
        url, filename = self.get_file_url(data_datetime)
        filepath = os.path.join(self.download_dir, filename)

        if not os.path.exists(filepath):
            print(f"Downloading: {url}")
            response = requests.get(url)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                print(f"Saved: {filepath}")
            else:
                print(f"Failed to download: {url}, status {response.status_code}")
                raise Exception("Download error")
        else:
            print(f"File already exists: {filepath}")

    def download_data_range(self, start_datetime, end_datetime, interval_minutes=10):
        current_datetime = start_datetime
        while current_datetime <= end_datetime:
            self.download_data(current_datetime)
            current_datetime += timedelta(minutes=interval_minutes)

# Example usage:
if __name__ == "__main__":
    dataset_type = "maxz_png"  # Change to desired dataset type
    download_dir = "~/chmi_data"  # Change to desired directory

    visualizer = ChmiRad(dataset_type=dataset_type, download_dir=download_dir)

    latest_datetime = datetime.now(dt.UTC).replace(second=0, microsecond=0)
    start_datetime = latest_datetime - timedelta(minutes=60)
    
    visualizer.download_data_range(start_datetime, latest_datetime, interval_minutes=5)

    # Example: Change dataset type dynamically
    visualizer.set_dataset_type("fct_maxz_tar")
    visualizer.download_data(latest_datetime)

    # Get available dataset types
    print("Available datasets:", ChmiRad.get_available_datasets())
