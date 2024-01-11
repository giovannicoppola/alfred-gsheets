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
import json




def write_plist_file(file_path, data):
    try:
        # Open the .plist file in binary mode and write the data
        with open(file_path, 'wb') as plist_file:
            plistlib.dump(data, plist_file)
        print(f"Changes written to '{file_path}' successfully.")
    except Exception as e:
        print(f"Error: Unable to write to '{file_path}'. {e}")

def plist2JSON (myPlistFile,myJSONFile):
    with open(myPlistFile, 'rb') as plist_file:
        plist_data = plistlib.load(plist_file)
    
    json_data = json.dumps(plist_data, indent = 4)

    with open(myJSONFile, 'w') as json_file:
        json_file.write(json_data)
    
    return plist_data


def json2plist(json_data, myPlistFile):
    
    with open(myPlistFile, 'wb') as plist_file:
        plistlib.dump(json_data, plist_file, fmt=plistlib.FMT_XML)  # FMT_XML for XML format

def editPlist (myPlistFile):
    with open(myPlistFile, 'rb') as plist_file:
        plist_json = plistlib.load(plist_file)
    
    




def cloneWorkflow():
    # Generate a random UUID string
    random_string = str(uuid.uuid4())
    toExclude = []

    # Create a new folder with the generated UUID as its name
    new_folder_name = f"{ALFRED_WORKFLOW_DIR}/giovanni-sheets_{random_string}"
    
    # Check if the folder already exists
    if os.path.exists(new_folder_name):
    # If it exists, remove it and its contents
        log ("folder exists, removing")
        #shutil.rmtree(new_folder_name)

    #os.makedirs(new_folder_name)
    log(f"creating directory {new_folder_name}")

    # Get the list of all items (files and directories) in the current directory
    current_items = os.listdir("sheetTemplate")

    for item in current_items:
        item_path = os.path.join(os.getcwd(), item)
        if item == 'info.plist':
            log ("found info.plist")
            with open(item, 'rb') as fp:
                myPlist = plistlib.load(fp)
                #log (myPlist)
                continue
        
        # Extract the filename from the path
        file_name = os.path.basename(item_path)
        # Check if the item is a file
        if os.path.isfile(item_path):
            # Copy the file to the new folder
            log (f"copying file {item_path}")
            #shutil.copy(item_path, os.path.join(new_folder_name, item))
        elif os.path.isdir(item_path):
            # Copy the entire directory to the new folder (including its contents)
            log (f"copying folder {item_path}")
            #shutil.copytree(item_path, os.path.join(new_folder_name, item))
            

    log(f"New folder '{new_folder_name}' created, and files/directories copied successfully.")


def printDone ():
    result = {"items": []}
            
    result["items"].append({
            "title": "Done!",
            'subtitle': "mySubTitle" ,
            'valid': True,
            "variables": {
                "URL_CHECK": "URL_CHECK"
                    },
            
            "icon": {
                "path": 'icon.png'
            },
            'arg': "myArg" 
                }) 
    print (json.dumps(result))  




if __name__ == "__main__":
    cloneWorkflow()
    #myData = plist2JSON ("sheetTemplate/info.plist","sheetTemplate/infoplist.json")
    #myData ['bundleid'] = 'cazacazacaza'
    #json2plist (myData,"sheetTemplate/info.plist")
    
    
    #myPrefs = plist2JSON ("sheetTemplate/prefs.plist","sheetTemplate/prefsplist.json")
    printDone()

