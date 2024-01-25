#!/usr/local/bin/python3


### entering values into a google sheet using a python script (which I can then launch from Alfred)
### Saturday, June 5, 2021, 8:32 PM
## 

## followed this tutorial (text saved in Evernote)
# https://www.makeuseof.com/tag/read-write-google-sheets-python/

## installed packages in python3
#python3 -m pip install oauth2client
#python3 -m pip install gspread




import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from google.oauth2 import service_account
import httplib2
from googleapiclient.discovery import build
import re



myURL = sys.argv[1]

from config import log, KEYFILE



def validateURL (myurl):
    """
    a function to validate the selected URL, list sheets, and check writing permissions
    """

    result = {"items": []}
    if "docs.google.com/spreadsheets" not in myurl:
        result["items"].append({
        
        "title": "⚠️ Not a Google Sheet!",
        "subtitle": myurl,
        "arg": "",
        "icon": {
            "path": ""
            }
            })
        print (json.dumps(result))
    
    else:
        sheetTitle, allSheets, lenHeads = get_sheet_list (myurl)
        writePermissions = checkPermissions (myurl)
        if writePermissions:
            writeP = "✅"
            writeS = ' and edit'
        else:
            writeP = "❌"
            writeS = ''
        result["items"].append({
        "title": "👍 This is a Google Sheet!",
        "subtitle": f"{sheetTitle} – Read ✅, Write {writeP}",
        "arg": "",
        "icon": {
            "path": ""
            }
            })

        if allSheets == "Permission Denied":
            result["items"].append({
                "title": "🛑 Permission denied!",
                "subtitle": "check spreadsheet permissions",
                "arg": "",
                "icon": {
                    "path": ""
                    }
            })

        else:
            for currSheet, currCol in zip (allSheets,lenHeads): 
                result["items"].append({
                "title": f"Clone alfred-sheets to browse{writeS}: {currSheet}",
            "subtitle": f"{sheetTitle} ▶️ {currSheet} estimated columns: {currCol}",
            "arg": "",
            "variables": {
                    "N_COLS": currCol,
                    "NEW_WORKSHEET_NAME": sheetTitle,
                    "NEW_URL": myurl,
                    "NEW_SHEET": currSheet,
                    "EST_COLS": currCol
                        },
                
            "icon": {
                "path": "icons/cloneIcon.png"
                }
                })
                
        
        print (json.dumps(result))
        
    
    return None


def countColumns (myurl):

    # Authenticate and open the Google Sheet
    gc = gspread.service_account()
    spreadsheet = gc.open('Your Spreadsheet Name')  # Replace with your actual spreadsheet name

    # Select a specific worksheet
    worksheet = spreadsheet.get_worksheet(0)  # Replace with the index or title of your worksheet

    # Get all non-empty cells in the worksheet
    all_cells = worksheet.get_all_values()

    # Calculate the maximum number of columns with data
    max_columns = max(len(row) for row in all_cells)

    print("Number of columns with data:", max_columns)




def checkPermissions (myURL):
        
    file_id = re.search(r"/d/([^/]*)/", myURL).group(1)  # Extract file ID from URL
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, ["https://www.googleapis.com/auth/drive"])
    http = credentials.authorize(httplib2.Http())
    service = build("drive", "v3", http=http)

    
    try:
        permissions = service.permissions().list(fileId=file_id).execute()
        
        for permission in permissions["permissions"]:
        
            if permission["role"] == "writer":
                writePermissions = True
                break
            
        else:
            writePermissions = False

    except:
        writePermissions = False
    
    return writePermissions



def get_sheet_list(spreadsheet_url, creds_path='burattinaio-105c8840e188.json'):
    try:
        # Authenticate with Google Sheets using credentials
        creds = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

        # Open the spreadsheet by URL
        gc = gspread.Client(auth=creds)
        gc.login()
        spreadsheet = gc.open_by_url(spreadsheet_url)

        # Get all sheets
        all_sheets = spreadsheet.worksheets()
        sheetTitle = spreadsheet.title
        # Print the names of each worksheet
        sheet_names = [worksheet.title for worksheet in all_sheets]
        
        log(f"Sheet names:{sheet_names}")
        log (f"sheet title: {sheetTitle}")
        # Get all non-empty cells in the worksheet
        all_cells = all_sheets[0].get_all_values()
         # Extract column headers (assuming the first row contains column headers)
        len_head = [len(sheet.row_values(1)) for sheet in all_sheets]

        # Calculate the maximum number of columns with data
        #max_columns = max(len(row) for row in all_cells)
        #log (f"max columns in first sheet: {max_columns} or {len_head}")
            
        return sheetTitle, sheet_names, len_head

    except Exception as e:
        log(f"An error occurred: {e}")
        return "Viewing: ❌, Writing: ❌","Permission Denied"









def fetchSheetProperties (myurl):

    
    # scopes = [
    # 'https://www.googleapis.com/auth/spreadsheets',
    # 'https://www.googleapis.com/auth/drive'
    # ]
    # credentials = ServiceAccountCredentials.from_json_keyfile_name("burattinaio-105c8840e188.json", scopes) 
    # #access the json key you downloaded earlier 

    # file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    try:
        
        active_sheet_name = get_active_sheet_name(myurl)

        if active_sheet_name:
            log(f"The active sheet is: {active_sheet_name}")
        else:
            log("Failed to retrieve the active sheet name.")

           
    
    except gspread.exceptions.SpreadsheetNotFound as e: 
        log ("caz!! ========")
    
    #worksheet = sheet.worksheet("Read")  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
    
    # Get all values from the worksheet
    #all_values = worksheet.get_all_values()
    # active_worksheet = sheet.worksheet(active_sheet_id)
    # active_sheet_name = active_worksheet.title
    return active_sheet_name
    
    

def fetchValues (mySource):
    result = {"items": []}
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("burattinaio-105c8840e188.json", scopes) 
    #access the json key you downloaded earlier 

    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    try:
        sheet = file.open("My Audiobooks")  #open sheet
        
    
    except gspread.exceptions.SpreadsheetNotFound as e: 
        log ("caz!! ========")
        resultErr= {"items": [{
        "title": "Error ",
        "subtitle": "Press Enter to check the instructions",
        "arg": "",
        "icon": {
            "path": ""
            }
            }]}
        print (json.dumps(resultErr))

        sys.exit(1)

    worksheet = sheet.worksheet("Read")  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
    # Get all values from the worksheet
    all_values = worksheet.get_all_values()
    
    
    # Extract column headers (assuming the first row contains column headers)
    column_headers = all_values[0]

    # Create a list to store dictionaries representing each row
    rows_as_list_of_dictionaries = []

       # Iterate through each row (excluding the header row) and create a dictionary
    for row in all_values[1:]:
        row_dict = {}
        for column_number in mySource:
            if 1 <= column_number <= len(column_headers):
                column_name = column_headers[column_number - 1]
                row_dict[column_name] = row[column_number - 1]
        rows_as_list_of_dictionaries.append(row_dict)

    log (rows_as_list_of_dictionaries)
    
    for myRow in rows_as_list_of_dictionaries:
        

        result["items"].append({
                "title": f"{myRow['Title']} ({myRow['Author']})",
                'subtitle': myRow['Year'],
                'valid': True,
                
            "mods": {
                    "alt": {
                        "valid": True,
                        "arg": "alfredapp.com/powerpack/",
                        "subtitle": "https://www.alfredapp.com/powerpack/"
                        },
                "cmd": {
                    "valid": True,
                    "arg": "alfredapp.com/shop/",
                    "subtitle": "https://www.alfredapp.com/shop/"
                        },
                "cmd+alt": {
                        "valid": True,
                        "arg": "alfredapp.com/blog/",
                        "subtitle": "https://www.alfredapp.com/blog/"
                        },
                },
                "icon": {
                    "path": 'icon.png'
                },
                'arg': "resultString"
                    }) 
    print (json.dumps(result))  

def fetchValuesPublic (mySource):
    result = {"items": []}
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("burattinaio-105c8840e188.json", scopes) 
    #access the json key you downloaded earlier 

    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    try:
        #sheet = file.open("My Audiobooks")  #open sheet
        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1ZW6TlsuGv7oQFEv8sryubIzYyQ8OFebY_1or7TYzrdY/edit#gid=1827593641'
        sheet = file.open_by_url(spreadsheet_url)
    
    except gspread.exceptions.SpreadsheetNotFound as e: 
        log ("caz!! ========")
        resultErr= {"items": [{
        "title": "Error ",
        "subtitle": "Press Enter to check the instructions",
        "arg": "",
        "icon": {
            "path": ""
            }
            }]}
        print (json.dumps(resultErr))

        sys.exit(1)

    worksheet = sheet.worksheet("Calories per 100g")  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1
    # Get all values from the worksheet
    all_values = worksheet.get_all_values()
    all_values = all_values[1:]
    
    # Extract column headers (assuming the first row contains column headers)
    column_headers = all_values[0]

    # Create a list to store dictionaries representing each row
    rows_as_list_of_dictionaries = []

       # Iterate through each row (excluding the header row) and create a dictionary
    for row in all_values[1:]:
        row_dict = {}
        for column_number in mySource:
            if 1 <= column_number <= len(column_headers):
                column_name = column_headers[column_number - 1]
                row_dict[column_name] = row[column_number - 1]
        rows_as_list_of_dictionaries.append(row_dict)

    log (rows_as_list_of_dictionaries)
    
    for myRow in rows_as_list_of_dictionaries:
        

        result["items"].append({
                "title": f"{myRow['Name']} ({myRow['Calories per serving']})",
                'subtitle': "myRow['']",
                'valid': True,
                
            "mods": {
                    "alt": {
                        "valid": True,
                        "arg": "alfredapp.com/powerpack/",
                        "subtitle": "https://www.alfredapp.com/powerpack/"
                        },
                "cmd": {
                    "valid": True,
                    "arg": "alfredapp.com/shop/",
                    "subtitle": "https://www.alfredapp.com/shop/"
                        },
                "cmd+alt": {
                        "valid": True,
                        "arg": "alfredapp.com/blog/",
                        "subtitle": "https://www.alfredapp.com/blog/"
                        },
                },
                "icon": {
                    "path": 'icon.png'
                },
                'arg': "resultString"
                    }) 
    print (json.dumps(result))  


def main ():
    #addValue (myValue,mySource)
    #fetchValues ([1,2,3,4])
    #fetchValuesPublic ([1,2,3])
    
    # # The URL of the public Google Sheet
    # spreadsheet_url = "https://docs.google.com/spreadsheets/d/1mnPLSFNf_t9-C4DOYxnVXIDU_G0hXDRf8kP2wLlkB8I/edit?pli=1#gid=0"

    # # Access the public Google Sheet and print the data
    # sheet_data = access_public_google_sheet(spreadsheet_url)

    # if sheet_data is not None:
    #     log(sheet_data)
    result = validateURL(myURL)
    



if __name__ == '__main__':
    main ()



