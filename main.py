import shutil #(for moving)
from abc import abstractmethod
from pathlib import Path
import os
from platform import system
from config import downloads
import filetype
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
        self.files = {}

    def get_folder_path(self):
        if self.system == "Windows": # Currently assumes folder will be in default location (not in OneDrive, etc.)
            return Path.home() / downloads["windows"]
        return None

    # Needs to be called optionally (only if folders do not already exist in specified location or if manually called)
    def create_folders(self):
        for folder in downloads["folders"]:
            dir_path = self.path / folder
            os.makedirs(dir_path, exist_ok=True) # Does not cause error if they already exist
            print(f"Folder created successfully in location: {dir_path}")

    # Currently assumes mime type will be identical to name of folders in config
    def register_file_types(self):
        for file in self.path.iterdir():
            if file.is_file(): # If file exists
                file_type = filetype.guess(file)
                if file_type:
                    details = file_type.mime.split("/")
                    related_folder, extension = details
                    if related_folder not in downloads["folders"]:
                        related_folder = "Misc"

                else:
                    extension = file.suffix if file.suffix else None
                    related_folder = "Misc"

                self.files[file.name] = {"folder": related_folder, "extension": extension}


    def move_files(self):
        for file in self.files.keys():
            folder = self.files[file]["folder"]
            source = self.path / file
            destination = self.path / folder / file
            shutil.move(str(source), str(destination))
            print(f"{file} moved to {folder} folder.")


class Program(OrganiseDownloads):
    def __init__(self):
        super().__init__()

    def check_for_folders(self):
        pass # return True/False

    def run(self):
        self.create_folders()
        self.register_file_types()
        self.move_files()


if __name__ == "__main__":
    Program().run()

# Automate with Task Scheduler for Windows?