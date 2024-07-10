import requests
import h5py
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

class ChmiRad:
    def __init__(self):
        self.base_url = "http://opendata.chmi.cz/meteorology/weather/radar/composite/pseudocappi2km/hdf5/T_PANV23_C_OKPR_{}.hdf"
        self.data_dict = {}
        self.latitudes = None
        self.longitudes = None
        self.tmp_dir = 'tmp'
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
    
    @staticmethod
    def format_datetime(dt):
        return dt.strftime('%Y%m%d%H%M%S')
    
    @staticmethod
    def round_down_to_nearest_five(dt):
        minute = (dt.minute // 5) * 5
        return dt.replace(minute=minute, second=0, microsecond=0)
    
    def download_data(self, data_datetime):
        formatted_datetime = self.format_datetime(data_datetime)
        url = self.base_url.format(formatted_datetime)
        filename = os.path.join(self.tmp_dir, f'pseudoCAPPI_2km_{formatted_datetime}.hdf5')
        
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
        
        self.load_data_from_file(data_datetime, filename)
    
    def download_data_range(self, start_datetime, end_datetime, interval_minutes=10):
        start_datetime = self.round_down_to_nearest_five(start_datetime)
        end_datetime = self.round_down_to_nearest_five(end_datetime)
        
        current_datetime = start_datetime
        while current_datetime <= end_datetime:
            self.download_data(current_datetime)
            current_datetime += timedelta(minutes=interval_minutes)
    
    def load_data_from_file(self, data_datetime, filename):
        try:
            with h5py.File(filename, 'r') as hdf:
                data = hdf['dataset1/data1/data'][:]  # Example path, adjust as necessary
                
                if self.latitudes is None or self.longitudes is None:
                    where_attrs = hdf['where'].attrs
                    LL_lat, LL_lon = where_attrs['LL_lat'], where_attrs['LL_lon']
                    UR_lat, UR_lon = where_attrs['UR_lat'], where_attrs['UR_lon']
                    xscale, yscale = where_attrs['xscale'], where_attrs['yscale']
                    xsize, ysize = where_attrs['xsize'], where_attrs['ysize']
                    
                    self.latitudes = np.linspace(LL_lat, UR_lat, ysize)
                    self.longitudes = np.linspace(LL_lon, UR_lon, xsize)
                    
                self.data_dict[data_datetime] = data
                
        except OSError as e:
            print(f"Error opening HDF5 file: {e}")
            raise e
        except KeyError as e:
            print(f"Error accessing data in HDF5 file: {e}")
            raise e
    
    def plot_data(self, data_datetime, prague_lat=50.0755, prague_lon=14.4378):
        data_datetime = self.round_down_to_nearest_five(data_datetime)
        
        if data_datetime not in self.data_dict:
            print(f"Data for {data_datetime} not found, downloading...")
            self.download_data(data_datetime)
        
        data = self.data_dict[data_datetime]
        
        fig = plt.figure(figsize=(10, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())

        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.LAKES, alpha=0.5)
        ax.add_feature(cfeature.RIVERS)

        extent = [self.longitudes.min(), self.longitudes.max(), self.latitudes.min(), self.latitudes.max()]
        im = ax.imshow(data, extent=extent, origin='upper', cmap='viridis', transform=ccrs.PlateCarree())

        ax.scatter(prague_lon, prague_lat, color='red', marker='o', label='Prague', transform=ccrs.PlateCarree())

        plt.colorbar(im, ax=ax, label='Reflectivity (dBZ)')
        plt.title(f'PseudoCAPPI 2km Reflectivity ({data_datetime})')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.legend()
        plt.show()

# Example usage:
if __name__ == "__main__":
    visualizer = ChmiRad()
    
    # Download and plot data for the last period (e.g., last 60 minutes) ending at the current time
    latest_datetime = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    start_datetime = latest_datetime - timedelta(minutes=60)
    visualizer.download_data_range(start_datetime, latest_datetime)
    
    # Plot data for a specific datetime (automatically downloads if not already downloaded)
    visualizer.plot_data(latest_datetime)
