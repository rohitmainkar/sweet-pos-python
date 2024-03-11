# updater.py

import sys
import os
import subprocess
import requests
import shutil
import time

VERSION_URL = "https://raw.githubusercontent.com/rohitmainkar/sweet-pos-python/main/posVersion.txt"
EXECUTABLE_URL = "https://github.com/rohitmainkar/sweet-pos-python/raw/main/test2.exe"
EXECUTABLE_PATH = "mainApp.exe"  # Assuming the current executable is named test2.exe
NEW_EXECUTABLE_PATH = "updated_executable.exe"  # Assuming the current executable is named test2.exe

class Updater:
    def __init__(self):
        self.new_executable_path = None

    def run(self):
        try:
            self.download_updated_executable()
            self.replace_executable()
            self.start_new_executable()
            self.close_old_executable()
            self.delete_new_executable()
        except Exception as e:
            print(f"An error occurred during update: {str(e)}")

    def download_updated_executable(self):
        response = requests.get(EXECUTABLE_URL, stream=True)
        with open(NEW_EXECUTABLE_PATH, "wb") as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)

    def replace_executable(self):
        # Move the newly downloaded executable to the location of the old executable
        shutil.move(NEW_EXECUTABLE_PATH, EXECUTABLE_PATH)

    def start_new_executable(self):
        # Start the newly updated executable
        subprocess.Popen([EXECUTABLE_PATH])

    def close_old_executable(self):
        # Close the current running instance of the updater executable gracefully
        sys.exit()

    def delete_new_executable(self):
        # Wait for a few seconds to ensure the new executable has started
        time.sleep(5)
        # Delete the downloaded executable (not needed anymore)
        os.unlink(NEW_EXECUTABLE_PATH)


if __name__ == "__main__":
    updater = Updater()
    updater.run()
