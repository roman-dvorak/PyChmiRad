# ChmiRad

ChmiRad is a tool for downloading and visualizing radar data from the Czech Hydrometeorological Institute (CHMI).

## Features

- Download radar reflectivity data from CHMI.
- Visualize the data using `matplotlib` and `cartopy`.
- Automatically handle temporary file storage.

## Installation

To install ChmiRad, clone this repository and install the dependencies using `pip3`.

```bash
git clone 
cd PyChmiRad
pip3 install .
```

## Usage

Here is an example of how to use ChmiRad:

```python
from chmirad import RadView
from datetime import datetime, timedelta

# Initialize the visualizer
visualizer = RadView()

# Download data for the last 60 minutes ending at the current time
latest_datetime = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
start_datetime = latest_datetime - timedelta(minutes=60)
visualizer.download_data_range(start_datetime, latest_datetime)

# Plot data for a specific datetime (automatically downloads if not already downloaded)
visualizer.plot_data(latest_datetime)
```