# main_app.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
import requests
import subprocess

VERSION_URL = "https://raw.githubusercontent.com/rohitmainkar/sweet-pos-python/main/posVersion.txt"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Application")
        self.setGeometry(100, 100, 400, 300)

        self.update_button = QPushButton("Check for Updates", self)
        self.update_button.setGeometry(50, 50, 300, 50)
        self.update_button.clicked.connect(self.check_for_updates)

    def check_for_updates(self):
        response = requests.get(VERSION_URL)
        remote_version = response.text.strip()
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
                # Run the updater executable
                subprocess.Popen(["updater.exe"])
                sys.exit()
        else:
            QMessageBox.information(
                None, "No Updates", "You have the latest version."
            )

    def get_local_version(self):
        with open("posVersion.txt", "r") as file:
            return file.read().strip()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
