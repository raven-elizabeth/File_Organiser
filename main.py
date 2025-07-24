import shutil
import sys
from abc import abstractmethod
from pathlib import Path
import os
from platform import system
from config import downloads, installers, code_programs, installer_deletion_countdown
import filetype
import time
from send2trash import send2trash
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
        self.validate_os()

    def validate_os(self):
        if not self.path:
            print("This program is currently unavailable for your OS.")
            sys.exit()

    def get_folder_path(self):
        if self.system == "Windows": # Currently assumes folder will be in default location (not in OneDrive, etc.)
            return Path.home() / downloads["windows"]
        return None

    # Needs to be called optionally (only if folders do not already exist in specified location or if manually called)
    def create_folders(self):
        for folder in downloads["folders"].values():
            dir_path = self.path / folder
            os.makedirs(dir_path, exist_ok=True) # Does not cause error if they already exist
            print(f"Folder created successfully in location: {dir_path}")

    @staticmethod
    def get_mime_details(file):
        if file.is_file(): # If file exists
            file_details = filetype.guess(file)
            if file_details: # If filetype guess succeeds
                details = file_details.mime.split("/")
                file_type, extension = details
            else:
                extension = file.suffix if file.suffix else None
                file_type = "misc"
            return file_type,extension
        return None, None

    # Currently assumes mime type will be identical to name of folders in config
    def register_file_types(self):
        for file in self.path.iterdir():
            file_type, extension = self.get_mime_details(file)

            if file_type not in downloads["folders"].keys():
                file_type = "misc"

            if extension in code_programs:
                file_type = "code"
            elif extension in installers:
                file_type = "installers"

            self.files[file.name] = {"folder": downloads["folders"][file_type], "extension": extension}

    @staticmethod
    def get_time_diff(file_path):
        date_last_modified = os.path.getmtime(file_path) # This provides last modification date & should work across platforms (gives number of seconds passed since)
        current_time = time.time()
        return current_time - date_last_modified

    def move_files(self):
        for file in self.files.keys():
            folder = self.files[file]["folder"]
            source = self.path / file
            destination = self.path / folder / file
            shutil.move(str(source), str(destination))
            print(f"{file} moved to {folder} folder.")

    def trash_old_files(self, folder_path):
        for file in folder_path:
            file_type, extension = self.get_mime_details(file)

            # Check for date of last modification & how long has passed in seconds
            if extension in installers:
                time_passed = self.get_time_diff(file)

                # Move file to recycle bin if it has not been modified in given amount of time
                if time_passed > installer_deletion_countdown:
                    send2trash(file)


class Program(OrganiseDownloads):
    def __init__(self):
        super().__init__()

    def run(self):
        self.create_folders()
        self.register_file_types()
        self.move_files()
        self.trash_old_files(self.path / "Setup Files")


if __name__ == "__main__":
    Program().run()

# Automate with Task Scheduler for Windows?
# For cross-platform functionality across operating systems, I will likely need to create classes for each OS with abstract methods