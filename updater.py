import sys
import os
import subprocess
import requests
import shutil
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QThread

# URL to download the updated executable
EXECUTABLE_URL = "https://github.com/rohitmainkar/sweet-pos-python/raw/main/test2.exe"

# Paths for the current and updated executables
EXECUTABLE_PATH = "mainApp.exe"
NEW_EXECUTABLE_PATH = "updated_executable.exe"

class Updater(QThread):
    # Signal to update progress bar
    progress_updated = pyqtSignal(float)

    def run(self):
        try:
            self.download_updated_executable()
            self.replace_executable()
            self.start_new_executable()
            self.delete_new_executable()
        except Exception as e:
            print(f"An error occurred during update: {str(e)}")

    def download_updated_executable(self):
        # Download the updated executable from the specified URL
        response = requests.get(EXECUTABLE_URL, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        bytes_downloaded = 0
        with open(NEW_EXECUTABLE_PATH, "wb") as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                bytes_downloaded += len(data)
                progress = (bytes_downloaded / total_size) * 100
                self.progress_updated.emit(progress)
                print(f"Download progress: {progress:.2f}%")
        print("Download completed.")

    def replace_executable(self):
        # Close the old executable before replacing it
        self.close_old_executable()
        # Move the newly downloaded executable to the location of the old executable
        shutil.move(NEW_EXECUTABLE_PATH, EXECUTABLE_PATH)

    def start_new_executable(self):
        # Start the updated executable
        subprocess.Popen([EXECUTABLE_PATH])

    def close_old_executable(self):
        # Close the current running instance of the updater executable
        os.system("TASKKILL /F /IM mainApp.exe")  # Terminate the process with the name "mainApp.exe"
        time.sleep(2)

    def delete_new_executable(self):
        time.sleep(5)  # Wait for a few seconds
        os.unlink(NEW_EXECUTABLE_PATH)  # Delete the downloaded executable
        os.system("TASKKILL /F /IM updater.exe")  # Terminate the process with the name "updater.exe"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Updater")
        self.setGeometry(100, 100, 400, 150)

        # Create and configure the progress bar
        self.progress_label = QLabel("Updating...", self)
        self.progress_label.setGeometry(10, 10, 380, 30)
        self.progress_label.setAlignment(Qt.AlignCenter)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 40, 380, 30)
        self.progress_bar.setValue(0)

        # Create the updater thread
        self.updater_thread = Updater()
        self.updater_thread.progress_updated.connect(self.update_progress)
        self.updater_thread.start()

    def update_progress(self, value):
        # Update the progress bar
        self.progress_bar.setValue(int(value))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
