import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f"File {event.src_path} has been modified")
        subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), path=".", recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
