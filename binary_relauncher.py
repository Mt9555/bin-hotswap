from dotenv import load_dotenv

from typing import Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen, CREATE_NEW_CONSOLE
import os
import time

load_dotenv()


class FileChangeHandler(FileSystemEventHandler):
    """Small tool to automatically relaunch a binary when a replacement is created."""

    def __init__(self, binary_path: str) -> None:
        super().__init__()
        self.binary_path: str = binary_path
        self.process: Optional[Popen] = None

    def on_created(self, event) -> None:
        if event.src_path == self.binary_path:
            print("Replacement binary created. Relaunching...")
            if self.process:
                self.process.terminate()
            self.process = Popen(self.binary_path, creationflags=CREATE_NEW_CONSOLE)


def init_file_monitoring(binary_path: str, monitored_directory: str) -> None:
    event_handler = FileChangeHandler(binary_path)
    observer = Observer()
    observer.schedule(event_handler, monitored_directory, recursive=False)
    observer.start()

    print(f"Monitoring directory: {monitored_directory}")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    """
    Monitor directory and automatically relaunch binary.

    Args:
        BINARY_PATH (str): Path to the actual binary.
        DIRECTORY_PATH (str): Directory to be monitored.

              Actual paths can be provided directly or loaded from environment variables.
    """

    binary_path = os.getenv("BINARY_PATH")
    directory_path = os.getenv("DIRECTORY_PATH")

    init_file_monitoring(binary_path, directory_path)
