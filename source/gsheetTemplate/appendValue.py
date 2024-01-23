import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re
import json
import gspread
import sys
from gspread.exceptions import APIError

from config import log, MY_SHEET,MY_URL, KEYFILE, APPEND_COLUMN

myString = sys.argv[1]

def checkPermissions (myURL):
    result = {"items": []}

    
    file_id = re.search(r"/d/([^/]*)/", myURL).group(1)  # Extract file ID from URL
    #log (file_id)


    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, ["https://www.googleapis.com/auth/drive"])
    http = credentials.authorize(httplib2.Http())
    service = build("drive", "v3", http=http)

    # Use the Drive API to get the file (spreadsheet) metadata
    file_metadata = service.files().get(fileId=file_id).execute()

    # Get the name of the worksheet (spreadsheet)
    worksheet_name = file_metadata['name']
    try:
        permissions = service.permissions().list(fileId=file_id).execute()
        
        for permission in permissions["permissions"]:
        
            if permission["role"] == "writer":
                myMessage = "👍 Write permissions granted"
                break
            
        else:
            myMessage = ("Write permission not granted")

    except:
        myMessage = "👎 CAZ"
    
    result["items"].append({
                "title": myMessage,
                'subtitle': worksheet_name,
                'valid': True,
                
                "icon": {
                    "path": 'icon.png'
                },
                'arg': ""
                    }) 
    print (json.dumps(result))  



def appendValue (myValue,myColumn):
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, scopes) 
    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    
    sheet = file.open_by_url(MY_URL)
    worksheet = sheet.worksheet(MY_SHEET)  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

    #firstRow = len(worksheet.col_values(0))
    lastrow = len(worksheet.col_values(myColumn))
    lastrow = lastrow+1
    try:
        # Attempt to update the cell
        worksheet.update_cell(lastrow, myColumn, myValue)
        print("Cell updated successfully!")

    except APIError as e:
        # Handle API errors
        print(f"APIError: {e}")
        
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")




def main ():
    #checkPermissions(MY_URL)
    
    appendValue (myString, APPEND_COLUMN)


if __name__ == '__main__':
    main ()


