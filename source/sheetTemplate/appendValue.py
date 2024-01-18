import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re
import json

from config import log, MY_SHEET,MY_URL, KEYFILE, APPEND_COLUMN


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



def addValue (myValue,mySource):
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, scopes) 
    #access the json key you downloaded earlier 

    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    sheet = file.open("Chiatto")  #open sheet
    worksheet = sheet.worksheet("weight")  #replace sheet_name with the name that corresponds to yours, e.g, it can be sheet1

    #firstRow = len(worksheet.col_values(0))
    lastrow = len(worksheet.col_values(mySource))
    lastrow = lastrow+1
    worksheet.update_cell(lastrow, mySource, myValue)


    #worksheet.update(['Test1'], range='B2:L6')

    #all_cells = sheet.range('A1:C6')
    #print(all_cells)

    #A1 = worksheet.acell('B2').value
    #print(A1)


def main ():
    checkPermissions(MY_URL)



if __name__ == '__main__':
    main ()


