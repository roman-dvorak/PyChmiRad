import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QTimer
from .mainwindow import Ui_MainWindow
from pychmirad import ChmiRad
from datetime import datetime, timedelta

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.rad_view = ChmiRad()

        # Connect buttons
        self.loadDataButton.clicked.connect(self.load_data)
        self.plotDataButton.clicked.connect(self.plot_data)

        # Timer for updating current location (mockup)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_location)
        self.timer.start(1000)

    def load_data(self):
        latest_datetime = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        start_datetime = latest_datetime - timedelta(minutes=60)
        self.rad_view.download_data_range(start_datetime, latest_datetime)
        self.statusbar.showMessage("Data loaded successfully")

    def plot_data(self):
        latest_datetime = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        self.rad_view.plot_data(latest_datetime)

    def update_location(self):
        # Mockup current location
        self.currentLocationLabel.setText("Current location: 50.0755, 14.4378")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
