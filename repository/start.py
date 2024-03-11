import sys
import os
import subprocess
import git
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer

REPO_PATH = '/path/to/your/repository'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto Version Updater")
        self.setGeometry(100, 100, 400, 300)

        self.update_button = QPushButton("Check for Updates", self)
        self.update_button.setGeometry(50, 50, 300, 50)
        self.update_button.clicked.connect(self.check_for_updates)

        # Create a timer to check for updates periodically
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.check_for_updates)
        self.update_timer.start(3600000)  # Check for updates every hour (3600000 milliseconds)

    def check_for_updates(self):
        try:
            repo = git.Repo(REPO_PATH)
            origin = repo.remotes.origin
            origin.fetch()

            # Get the latest commit hash from the remote repository
            latest_commit_hash_remote = origin.refs.master.commit.hexsha

            # Get the current commit hash of the local repository
            latest_commit_hash_local = repo.head.commit.hexsha

            if latest_commit_hash_remote != latest_commit_hash_local:
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
        try:
            # Download the updated executable or any necessary files
            # For simplicity, we assume the updated executable is in the repository

            # Replace the current executable with the updated one
            os.replace(os.path.join(REPO_PATH, 'your_executable'), sys.executable)

            # Show dialog box message while updating
            updating_dialog = QMessageBox(self)
            updating_dialog.setWindowTitle("Updating")
            updating_dialog.setText("Updating application...")
            updating_dialog.exec_()

            # Restart the application using the updated executable
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during update: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
