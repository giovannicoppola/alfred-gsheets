"""
CloneSheets
A script to clone the current workflow to create a new one
Part of the alfred-sheets Workflow
Giovanni Coppola
Sunny ☀️   🌡️+74°F (feels +77°F, 56%) 🌬️↘2mph 🌒&m Sat Jul 22 10:57:18 2023
W29Q3 – 203 ➡️ 161 – 72 ❇️ 293
"""

import os
import shutil
import uuid
from config import log, ALFRED_WORKFLOW_DIR
import plistlib



def write_plist_file(file_path, data):
    try:
        # Open the .plist file in binary mode and write the data
        with open(file_path, 'wb') as plist_file:
            plistlib.dump(data, plist_file)
        print(f"Changes written to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error: Unable to write to '{file_path}'. {e}")
        
def cloneWorkflow():
    # Generate a random UUID string
    random_string = str(uuid.uuid4())

    # Create a new folder with the generated UUID as its name
    new_folder_name = f"{ALFRED_WORKFLOW_DIR}/giovanni-sheets_{random_string}"
    #os.makedirs(new_folder_name)

    # Get the list of all items (files and directories) in the current directory
    current_items = os.listdir()

    for item in current_items:
        item_path = os.path.join(os.getcwd(), item)
        if item == 'info.plist':
            log ("found info.plist")
            with open(item, 'rb') as fp:
                myPlist = plistlib.load(fp)
                log (myPlist)
                continue

        # Check if the item is a file
        if os.path.isfile(item_path):
            # Copy the file to the new folder
            log ("skipped file")
            #shutil.copy(item_path, os.path.join(new_folder_name, item))
        elif os.path.isdir(item_path):
            # Copy the entire directory to the new folder (including its contents)
            #shutil.copytree(item_path, os.path.join(new_folder_name, item))
            log ("skipped dir")

    log(f"New folder '{new_folder_name}' created, and files/directories copied successfully.")



if __name__ == "__main__":
    cloneWorkflow()
