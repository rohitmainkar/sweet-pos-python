import sys
import os
import subprocess
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QProgressBar,
)
from PyQt5.QtCore import pyqtSignal, QObject
import shutil
import time

VERSION_URL = "https://raw.githubusercontent.com/rohitmainkar/sweet-pos-python/main/posVersion.txt"
EXECUTABLE_URL = "https://github.com/rohitmainkar/sweet-pos-python/raw/main/test2.exe"
EXECUTABLE_PATH = "updated_executable.exe"

class Updater(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def run(self):
        try:
            remote_version = self.get_remote_version()
            local_version = self.get_local_version()

            if remote_version != local_version:
                reply = QMessageBox.question(
                    None,
                    "Update Available",
                    "New version available. Do you want to update?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )

                if reply == QMessageBox.Yes:
                    self.download_updated_executable()
                    self.finished.emit()
            else:
                QMessageBox.information(
                    None, "No Updates", "You have the latest version."
                )
        except Exception as e:
            error_message = f"An error occurred during update: {str(e)}"
            self.error.emit(error_message)

    def get_remote_version(self):
        response = requests.get(VERSION_URL)
        response.raise_for_status()
        return response.text.strip()

    def get_local_version(self):
        with open("posVersion.txt", "r") as file:
            return file.read().strip()

    def download_updated_executable(self):
        response = requests.get(EXECUTABLE_URL, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        with open(EXECUTABLE_PATH, "wb") as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto Version Updater")
        self.setGeometry(100, 100, 400, 300)

        self.update_button = QPushButton("Check for Updates", self)
        self.update_button.setGeometry(50, 50, 300, 50)
        self.update_button.clicked.connect(self.check_for_updates)

    def check_for_updates(self):
        updater = Updater()
        updater.finished.connect(self.on_update_finished)
        updater.error.connect(self.show_error)
        updater.progress.connect(self.update_progress)
        updater.run()

    def on_update_finished(self):
        QMessageBox.information(
            None, "Update Finished", "Application updated successfully."
        )
        self.replace_and_start_executables()

    def show_error(self, error_message):
        print("Error", f"An error occurred during update: {error_message}")
        QMessageBox.critical(
            None, "Error", f"An error occurred during update: {error_message}"
        )

    def update_progress(self, value):
        # Handle progress update here if needed
        pass

    def replace_and_start_executables(self):
        # Step 1: Replace the old executable with the new one
        new_executable_path = EXECUTABLE_PATH
        old_executable_path = "test2.exe"  # Assuming the old executable name is test2.exe
        if os.path.exists(new_executable_path):
            shutil.move(new_executable_path, old_executable_path)

            # Step 2: Start the new executable
            subprocess.Popen([old_executable_path])

            # Step 3: Wait for the new executable to start and then close it
            time.sleep(5)  # Adjust the duration as needed
            subprocess.Popen(["taskkill", "/f", "/im", old_executable_path])

            # Step 4: Start the old executable again
            subprocess.Popen([old_executable_path])

            # Step 5: Delete the new executable
            os.unlink(old_executable_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
