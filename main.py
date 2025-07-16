# import shutil (for moving)
from abc import abstractmethod
from pathlib import Path
import os
from platform import system
from config import downloads
# import googletrans possible to translate name of folders according to language


class System:
    def __init__(self):
        self.system = system() # User's operating system

    @abstractmethod
    def get_folder_path(self):
        pass


class OrganiseDownloads(System):
    def __init__(self):
        super().__init__()
        self.path = self.get_folder_path()

    def get_folder_path(self):
        if self.system == "Windows": # Currently assumes folder will be in default location (not in OneDrive, etc.)
            return Path.home() / downloads["windows"]
        else:
            return None

    # Needs to be called optionally (only if folders do not already exist in specified location or if manually called)
    def create_folders(self):
        for folder in downloads["folders"]:
            dir_path = f"{self.path}/{folder}"
            os.makedirs(dir_path)
            print(f"Folder created successfully in location: {dir_path}")

    # Currently assuming file has an extension
    def get_file_type(self):
        for file in self.path:
            extension = Path(file).suffix
            if extension:
                pass # Can I use filetypes or mimetypes or alt to get list of possible extensions, rather than making my own dictionary?

    def move_files(self):
        pass


def run():
    pass


if __name__ == "__main__":
    run()