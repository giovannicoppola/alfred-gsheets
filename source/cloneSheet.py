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

MyNewURL = os.getenv('NEW_URL')
    


def plist2JSON (myPlistFile,myJSONFile):
    with open(myPlistFile, 'rb') as plist_file:
        plist_data = plistlib.load(plist_file)
    
    json_data = json.dumps(plist_data, indent = 4)

    with open(myJSONFile, 'w') as json_file:
        json_file.write(json_data)
    
    return plist_data



def editPlist (myPlistFile, newPlist):
    with open(myPlistFile, 'rb') as plist_file:
        plist_json = plistlib.load(plist_file)
    try:
        
        #myData = plist2JSON ("gsheetTemplate/info.plist","gsheetTemplate/infoplist.json")
        #myData = plist2JSON ("gsheetTemplate/info.plist")
        plist_json ['bundleid'] = 'cazzonecacatone'
        log (f"UUUUUUUUURL: {MyNewURL}")
        #json2plist (myData,"gsheetTemplate/info.plist")
        
        # Open the .plist file in binary mode and write the data
        with open(newPlist, 'wb') as plist_file:
            plistlib.dump(plist_json, plist_file, fmt=plistlib.FMT_XML)  # FMT_XML for XML format
            #plist_json.dump(myData, plist_file)

        #myPrefs = plist2JSON ("gsheetTemplate/prefs.plist","gsheetTemplate/prefsplist.json")
        log(f"Changes written to '{newPlist}' successfully.")
    except Exception as e:
        log(f"Error: Unable to write to '{newPlist}'. {e}")
    



def cloneWorkflow():
    # Generate a random UUID string
    random_string = str(uuid.uuid4())
    random_string = "testingtesting"
    
    newBundleID = f"giovanni-gsheets_{random_string}"
    new_folder_name = f"{ALFRED_WORKFLOW_DIR}/{newBundleID}"
    
    # Remove the folder already exists
    if os.path.exists(new_folder_name):
        log ("folder exists, removing")
        shutil.rmtree(new_folder_name)

    log(f"creating directory {new_folder_name}")
    os.makedirs(new_folder_name)
    

    # Get the list of all items (files and directories) in the template directory
    current_items = os.listdir("gsheetTemplate")

    for item in current_items:
        item_path = os.path.join("gsheetTemplate", item)
        new_item_path = os.path.join(new_folder_name, item)
        
        # Extract the filename from the path
        file_name = os.path.basename(item_path)
        # Check if the item is a file
        if os.path.isfile(item_path):
            if item == 'info.plist':
            # insert the plist editing here
                editPlist (item_path,new_item_path)
                log ("found info.plist")
                continue

            elif item == 'prefs.plist':
                # insert the prefs editing here
                log ("found prefs.plist")
                continue
                
            else:
                # Copy the file to the new folder
                log (f"copying file {item_path}")
                shutil.copy(item_path, os.path.join(new_folder_name, item))

        elif os.path.isdir(item_path):
            # Copy the entire directory (including its contents) to the new folder (including its contents)
            log (f"copying folder {item_path}")
            shutil.copytree(item_path, os.path.join(new_folder_name, item))
            

    log(f"New folder '{new_folder_name}' created, and files/directories copied successfully.")


def printDone ():
    result = {"items": []}
            
    result["items"].append({
            "title": "✅ Done!",
            'subtitle': "press ↩️ to open the new workflow configuration, or Esc to exit" ,
            'valid': True,
            "variables": {
                "myBundleID": "cazacazacaza"
                    },
            
            "icon": {
                "path": 'icon.png'
            },
            'arg': "myArg" 
                }) 
    print (json.dumps(result))  




if __name__ == "__main__":
    cloneWorkflow()
    
    printDone()

