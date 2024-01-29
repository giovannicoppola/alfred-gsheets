"""
Appending a value to a Google Sheet with writing privileges
Part of the gsheet workflow

"""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
import gspread
import sys


from config import log, MY_SHEET,MY_URL, KEYFILE, APPEND_COLUMN

myString = sys.argv[1]

def printError (myMessage, mySubtitle = "Check debugger for details"):
    result = {"items": []}
            
    result["items"].append({
            "title": f"ERROR 🚨 {myMessage}",
            'subtitle':  mySubtitle,
            'valid': True,
            "variables": {
                
                    },
            
            "icon": {
                "path": 'icon.png'
            },
            'arg': "myArg" 
                }) 
    print (json.dumps(result))  
    sys.exit(1)

def appendValue (myValue,myColumn):
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, scopes) 
    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    
    sheet = file.open_by_url(MY_URL)
    worksheet = sheet.worksheet(MY_SHEET)  

    
    lastrow = len(worksheet.col_values(myColumn))
    lastrow = lastrow+1
    try:
        # Attempt to update the cell
        worksheet.update_cell(lastrow, myColumn, myValue)
        print("✅ done!")
        

    except gspread.exceptions.APIError as e:
        # Handle API errors
        error_data = json.loads(e.response.text)
        errorStatus  = f"🚨 {error_data['error']['status']}"
        log(errorStatus)
        print(errorStatus)
        
        
    except Exception as e:
        # Handle other exceptions
        log(f"APIError: {e}")
        printError(e)
        




def main ():
    if not APPEND_COLUMN:
        printError ("Append column not set")
    else:
        appendValue (myString, APPEND_COLUMN)


if __name__ == '__main__':
    main ()


