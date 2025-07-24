import shutil #(for moving)
import sys
from abc import abstractmethod
from pathlib import Path
import os
from platform import system
from config import downloads, installers, code_programs
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

    # Currently assumes mime type will be identical to name of folders in config
    def register_file_types(self):
        for file in self.path.iterdir():
            if file.is_file(): # If file exists
                file_details = filetype.guess(file)
                if file_details: # If filetype guess succeeds
                    details = file_details.mime.split("/")
                    print(details)
                    file_type, extension = details
                    if file_type not in downloads["folders"].keys():
                        file_type = "misc"

                else:
                    extension = file.suffix if file.suffix else None
                    file_type = "misc"

                if extension in installers:
                    # Check for date of download & how long has passed (2 weeks = delete)
                    pass

                elif extension in code_programs:
                    file_type = "code"

                self.files[file.name] = {"folder": downloads["folders"][file_type], "extension": extension}
                print(file_type)

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

    def run(self):
        self.create_folders()
        self.register_file_types()
        self.move_files()


if __name__ == "__main__":
    Program().run()

# Automate with Task Scheduler for Windows?
# Check for .exe (executables & installers) (application folder)
# Check for code files