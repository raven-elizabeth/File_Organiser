downloads = {
    "windows": "Downloads", # Rename if your downloads folder is called something else
    "folders": [{"image": "Images"}, # Edit sub-folder names by changing the values if preferred
                {"video": "Videos"},
                {"audio": "Audio"},
                {"application", "Documents"},
                {"misc": "Misc"},
                {"code": "Code"},
                {"installers": "Setup Files"}]
}

code_programs = [".py", ".js", ".java", ".sql", ".cs", ".php", ".go", ".mongodb", ".ts", ".rb", ".cpp", ".c"] # Add extensions for code/database files here


installers = [".exe", ".msi", ".pkg", ".dmg", ".deb", ".rpm"] # These files will be deleted after a set time period (intended use for setup/installer files that are no longer needed)
installer_deletion_countdown = 1209600 # Default value 1,209,600 is 2 weeks

# Could add language choice later