import shutil
from abc import abstractmethod
from pathlib import Path
import os
from platform import system


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
        if self.system == "Windows":
            pass
        else:
            return None


def run():
    pass


if __name__ == "__main__":
    run()