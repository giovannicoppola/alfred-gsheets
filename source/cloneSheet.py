"""
CloneSheet
A script to clone the current workflow to create a new one
Part of the alfred-sheets Workflow
Giovanni Coppola
Sunny ☀️   🌡️+74°F (feels +77°F, 56%) 🌬️↘2mph 🌒&m Sat Jul 22 10:57:18 2023
W29Q3 – 203 ➡️ 161 – 72 ❇️ 293
"""

import os
import shutil
import uuid
from config import log, ALFRED_WORKFLOW_DIR, KEYFILE
import plistlib
import json
import time

MyNewURL = os.getenv('NEW_URL')
MyNewSheet = os.getenv('NEW_SHEET')
MyEstimatedColumns = os.getenv('EST_COLS')
NewWorksheetName = os.getenv('NEW_WORKSHEET_NAME')
NumberColumns = int(os.getenv('N_COLS'))
WriteP = int(os.getenv('WRITE_P'))

# Generate a random UUID string
random_string = str(uuid.uuid4())
newBundleID = f"giovanni-gsheets_{random_string}"



def plist2JSON ():
    """
    worker function to export plist files to JSON for troubleshooting
    
    """
    with open('gsheetTemplate/info.plist', 'rb') as plist_file:
        plist_data = plistlib.load(plist_file)
    
    json_data = json.dumps(plist_data, indent = 4)

    with open('gsheetTemplate/infoplist.json', 'w') as json_file:
        json_file.write(json_data)
    
    with open('gsheetTemplate/prefs.plist', 'rb') as plist_file:
        plist_data = plistlib.load(plist_file)
    
    json_data = json.dumps(plist_data, indent = 4)

    with open('gsheetTemplate/prefsplist.json', 'w') as json_file:
        json_file.write(json_data)
    

def editPrefs (myPrefFile, newPref):
    # setting default columns based on the number of columns in the sheet
    if NumberColumns > 2:
        SubtitleCol = 2    
        ArgCol = 3
    elif NumberColumns > 1:
        SubtitleCol = ArgCol = 2    
    
    with open(myPrefFile, 'rb') as plist_file:
        plist_json = plistlib.load(plist_file)
    try:
        
        # Setting default columns if ncol >1 (all are 1 by default)
        if NumberColumns > 1:
            plist_json ["ARG_COLUMN"] = str(ArgCol)
            plist_json  ["SUBTITLE_COLUMN"] = str(SubtitleCol)
            
        
        # Setting the APPEND column if the user has writing privileges
        if WriteP:
            plist_json ["APPEND_COLUMN"] = "1"
            
        
        # Open the .plist file in binary mode and write the data
        with open(newPref, 'wb') as plist_file:
            plistlib.dump(plist_json, plist_file, fmt=plistlib.FMT_XML)  # FMT_XML for XML format
        
        
        log(f"Changes written to '{newPref}' successfully.")
    except Exception as e:
        log(f"Error: Unable to write to '{newPref}'. {e}")
    

def editInfo (myInfoFile, newInfo,newBundleID):

## choosing a worksheet name and keyword
    words = NewWorksheetName.split()

    if len(words) > 0:
        # If there is a space, return the first word
        myfirstWord = words[0]
    else:
        # If no space, return the first three letters
        myfirstWord = NewWorksheetName[:3].casefold()
    myWorkflowName = f'gsheets-{myfirstWord}'
    
    
        

    with open(myInfoFile, 'rb') as plist_file:
        plist_json = plistlib.load(plist_file)
    try:
        
        plist_json ['description'] = f"Browse a Google Sheet: {NewWorksheetName}"
        plist_json ['bundleid'] = newBundleID
        plist_json ['name'] = myWorkflowName
        
        
        # Setting MY_URL
        plist_json['userconfigurationconfig'] = [
            {**item, "config": {**item["config"], "default": MyNewURL}} if item["variable"] == "MY_URL" else item
            for item in plist_json["userconfigurationconfig"]
        ]

        # Setting MY_SHEET
        plist_json['userconfigurationconfig'] = [
            {**item, "config": {**item["config"], "default": MyNewSheet}} if item["variable"] == "MY_SHEET" else item
            for item in plist_json["userconfigurationconfig"]
        ]

        # Setting MAIN_KEYWORD (default: first 3 letters of Worksheet name)
        plist_json['userconfigurationconfig'] = [
            {**item, "config": {**item["config"], "default": NewWorksheetName[:3].casefold()}} if item["variable"] == "MAIN_KEYWORD" else item
            for item in plist_json["userconfigurationconfig"]
        ]

        # Setting the  APPEND keyword  if the user has writing privileges
        if WriteP:
            plist_json['objects'] = [
                {**item, "config": {**item["config"], "keyword": "{var:MAIN_KEYWORD}::append"}} if item["uid"] == "E43256F1-8519-491C-B9C8-32173EEF23CD" else item
                for item in plist_json["objects"]
                ]
        
        # Setting the workflow name in readme
        myReadme = plist_json ['readme']
        newREADME = myReadme.replace("[[New workflow name]]", myWorkflowName)
        plist_json ['readme'] = newREADME

        # Setting key file
        plist_json['userconfigurationconfig'] = [
            {**item, "config": {**item["config"], "default": KEYFILE}} if item["variable"] == "KEYFILE" else item
            for item in plist_json["userconfigurationconfig"]
        ]
        
        # Open the .plist file in binary mode and write the data
        with open(newInfo, 'wb') as plist_file:
            plistlib.dump(plist_json, plist_file, fmt=plistlib.FMT_XML)  # FMT_XML for XML format
            

        
        log(f"Changes written to '{newInfo}' successfully.")
    except Exception as e:
        log(f"Error: Unable to write to '{newInfo}'. {e}")
    



def cloneWorkflow():
    new_folder_name = f"{ALFRED_WORKFLOW_DIR}/{newBundleID}"
    
    # Remove the folder if already exists
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
            # editing info.plist
                editInfo (item_path,new_item_path, newBundleID)
                log ("edited info.plist")
                continue

            elif item == 'prefs.plist':
                # editing prefs.plist
                editPrefs (item_path,new_item_path)
                log ("edited prefs.plist")
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
            "title": f"✅ Done! Use '{NewWorksheetName[:3].casefold()}' to launch",
            'subtitle': "press ↩️ to open the new workflow configuration, or Esc to exit" ,
            'valid': True,
            "variables": {
                "myBundleID": newBundleID
                    },
            
            "icon": {
                "path": 'icon.png'
            },
            'arg': "myArg" 
                }) 
    print (json.dumps(result))  




if __name__ == "__main__":
    #plist2JSON ()
    cloneWorkflow()
    time.sleep (1) 
    printDone()

