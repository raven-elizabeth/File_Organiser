import shutil
from abc import abstractmethod
from pathlib import Path
import os
from platform import system
from config import downloads


class System:
    def __init__(self):
        self.system = system() # User's operating system

    @abstractmethod
    def get_folder_path(self):
        pass


class OrganiseDownloads(System):
    def __init__(self):
        super().__init__()

    def get_folder_path(self):
        if self.system == "Windows": # Currently assumes folder will be in default location (not in OneDrive, etc.)
            return Path.home() / downloads["windows"]
        else:
            return None


def run():
    pass


if __name__ == "__main__":
    run()