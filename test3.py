import sys
import os
import subprocess
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QProgressBar
from PyQt5.QtCore import QTimer, QObject, QThread, pyqtSignal
import git
import shutil

# URL of the posVersion.txt file on GitHub
VERSION_URL = 'https://raw.githubusercontent.com/rohitmainkar/sweet-pos-python/main/posVersion.txt'
REPO_URL = 'https://github.com/rohitmainkar/sweet-pos-python.git'
EXECUTABLE_PATH = 'test2.exe'

class Updater(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)  # Define error signal
    progress = pyqtSignal(int)  # Define progress signal

    def run(self):
        try:
            if os.path.exists('repository'):
                shutil.rmtree('repository')

            repo = git.Repo.clone_from(REPO_URL, 'repository')

            origin = repo.remotes.origin
            origin.fetch()
            total_steps = len(list(origin.refs))

            # Perform updates step by step
            for i, commit in enumerate(origin.refs):
                origin.pull(commit)
                self.progress.emit((i + 1) * 100 // total_steps)  # Emit progress signal
                QApplication.processEvents()  # Process events to keep UI responsive

            os.replace(os.path.join('repository', EXECUTABLE_PATH), 'updated_executable.exe')

            self.finished.emit()  # Signal that the update is finished

        except git.exc.GitCommandError as e:
            error_message = f"Git command error occurred during update: {str(e)}"
            self.error.emit(error_message)  # Emit error signal

        except Exception as e:
            error_message = f"An error occurred during update: {str(e)}"
            self.error.emit(error_message)  # Emit error signal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto Version Updater")
        self.setGeometry(100, 100, 400, 300)

        self.update_button = QPushButton("Check for Updates", self)
        self.update_button.setGeometry(50, 50, 300, 50)
        self.update_button.clicked.connect(self.check_for_updates)

        # Progress bar to show update progress
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(50, 120, 300, 30)

        # Create a timer to check for updates periodically
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.check_for_updates)
        self.update_timer.start(3600000)  # Check for updates every hour (3600000 milliseconds)

        self.updater_thread = QThread()
        self.updater = Updater()
        self.updater.moveToThread(self.updater_thread)
        self.updater_thread.started.connect(self.updater.run)
        self.updater.finished.connect(self.on_update_finished)
        self.updater.error.connect(self.show_error)  # Connect error signal
        self.updater.progress.connect(self.update_progress)  # Connect progress signal
        self.updater_thread.start()

    def check_for_updates(self):
        try:
            # Fetch the version number from the URL
            response = requests.get(VERSION_URL)
            response.raise_for_status()  # Raise an exception for HTTP errors
            remote_version = response.text.strip()

            # Get the current version from the local file
            with open('posVersion.txt', 'r') as file:
                local_version = file.read().strip()

            if remote_version != local_version:
                reply = QMessageBox.question(self, 'Update Available',
                                             "New version available. Do you want to update?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    self.update_application()

            else:
                QMessageBox.information(self, "No Updates", "You have the latest version.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def update_application(self):
        self.update_button.setEnabled(False)

    def on_update_finished(self):
        self.update_button.setEnabled(True)
        QMessageBox.information(None, "Update Finished", "Application updated successfully.")

    def show_error(self, error_message):
        print("Error", f"An error occurred during update: {error_message}")
        QMessageBox.critical(None, "Error", f"An error occurred during update: {error_message}")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def closeEvent(self, event):
        if self.updater_thread.isRunning():
            self.updater_thread.quit()
            self.updater_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
