
"""
checkSheet
part of the gsheets workflow
checks that a website is a google sheet, checks privileges, fetches sheet names
"""


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
            writeBool = True
        else:
            writeP = "❌"
            writeS = ''
            writeBool = False
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
            sheetCounter = 1
            sheetTotal = len (allSheets)
            for currSheet, currCol in zip (allSheets,lenHeads): 
                result["items"].append({
                    "title": f"Clone alfred-sheets to browse{writeS}: {currSheet}",
                    "subtitle": f"{sheetCounter}/{sheetTotal} {sheetTitle} ▶️ {currSheet} – estimated n. columns: {currCol}",
                    "arg": "",
                    "variables": {
                            "N_COLS": currCol,
                            "NEW_WORKSHEET_NAME": sheetTitle,
                            "NEW_URL": myurl,
                            "NEW_SHEET": currSheet,
                            "EST_COLS": currCol,
                            "WRITE_P": writeBool,
                                },
                        
                    "icon": {
                    "path": "icons/cloneIcon.png"
                }
                })
                sheetCounter += 1 
        
        print (json.dumps(result))
        
    
    return None




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


def get_sheet_list(spreadsheet_url, creds_path=KEYFILE):
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
        
        # Fetch the name of each worksheet
        sheet_names = [worksheet.title for worksheet in all_sheets]
        
        #log(f"Sheet names:{sheet_names}")
        #log (f"sheet title: {sheetTitle}")
        
        # Get all non-empty cells in the worksheet
        all_cells = all_sheets[0].get_all_values()
        
        # Extract column headers (assuming the first row contains column headers)
        len_head = [len(sheet.row_values(1)) for sheet in all_sheets]

            
        return sheetTitle, sheet_names, len_head

    except Exception as e:
        log(f"An error occurred: {e}")
        return "Viewing: ❌, Writing: ❌","Permission Denied"




def main ():
    validateURL(myURL)
    

if __name__ == '__main__':
    main ()



