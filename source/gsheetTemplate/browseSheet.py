#!/usr/local/bin/python3
# encoding: utf-8

# Overcast ☁️   🌡️+40°F (feels +34°F, 55%) 🌬️↘6mph 🌗&m Wed Jan  3 18:13:05 2024
# W1Q1 – 3 ➡️ 362 – 237 ❇️ 128

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
import re
from oauth2client.service_account import ServiceAccountCredentials
import json
from google.oauth2 import service_account
from urllib.parse import urlparse
from config import HEADER_ROW, MY_SHEET,MY_URL, TITLE_COLUMN, SUBTITLE_COLUMN, ARG_COLUMN, LAYOUT_LIST,KEYFILE, log

#myValue = sys.argv[2]
#mySource = list(range(1, 12))
mySource = [TITLE_COLUMN+1, SUBTITLE_COLUMN+1, ARG_COLUMN+1]

MYINPUT = sys.argv[1].casefold()

# toShow = [item for item in toShow if (
    
#     all(substring.casefold() in item['content'].casefold() for substring in mySearchStrings)
#     )]


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
        # Print the names of each worksheet
        sheet_names = [worksheet.title for worksheet in all_sheets]
        log(f"Sheet names:{sheet_names}")

        
        return sheet_names

    except Exception as e:
        log(f"An error occurred: {e}")
        return "Permission Denied"


def printError ():
    result = {"items": []}
            
    result["items"].append({
            "title": f"ERROR🚨",
            'subtitle': "DETAILS" ,
            'valid': True,
            "variables": {
                
                    },
            
            "icon": {
                "path": 'icon.png'
            },
            'arg': "myArg" 
                }) 
    print (json.dumps(result))  



def replace_fields(original_string, series_list,column_headers):
    # Find all occurrences of "[index]" in the original string
    placeholders = [int(index) for index in re.findall(r'\[(\d+)\]', original_string)]
    
    # Replace each placeholder with the corresponding value from the series_list
    replaced_string = original_string
    for index in placeholders:
        if 0 <= index < len(series_list):
            replaced_string = replaced_string.replace(f'[{index}]', str(series_list[column_headers[index-1]]))

    return replaced_string




def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # Check if both scheme and netloc are present
    except ValueError:
        return False  # Invalid URL format




def fetchValues (spreadsheet_url):
    result = {"items": []}
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEYFILE, scopes) 
    

    file = gspread.authorize(credentials) # authenticate the JSON key with gspread
    try:
        sheet = file.open_by_url(spreadsheet_url)
    
    except gspread.exceptions.SpreadsheetNotFound as e: 
        log ("======== Error ========")
        resultErr= {"items": [{
        "title": "⚠️ Error",
        "subtitle": "Press Enter to check the instructions",
        "arg": "",
        "icon": {
            "path": ""
            }
            }]}
        print (json.dumps(resultErr))

        sys.exit(1)

    worksheet = sheet.worksheet(MY_SHEET) 
    
    # Get all values from the worksheet
    all_values = worksheet.get_all_values()
    


    # Extract column headers (assuming the first row contains column headers)
    column_headers = all_values[HEADER_ROW]
    #log (column_headers)

    # # Extract the desired columns
    #selected_columns = [[row[i] for i in mySource] for row in all_values]
    #log (selected_columns)

    # Create a list to store dictionaries representing each row
    rows_as_list_of_dictionaries = []

       # Iterate through each row (excluding the header row) and create a dictionary
    for row in all_values[HEADER_ROW+1:]:
        row_dict = {}
        for column_number in mySource:
            if 1 <= column_number <= len(column_headers):
                column_name = column_headers[column_number - 1]
                row_dict[column_name] = row[column_number - 1]
        rows_as_list_of_dictionaries.append(row_dict)

    #log (rows_as_list_of_dictionaries)
    log (LAYOUT_LIST)
    
    for myRow in rows_as_list_of_dictionaries:
        
        if LAYOUT_LIST:
            myTitle = replace_fields(LAYOUT_LIST[0],myRow,column_headers)
            mySubTitle = replace_fields(LAYOUT_LIST[1],myRow,column_headers)
            myArg = replace_fields(LAYOUT_LIST[2],myRow,column_headers)
        else:
            myTitle = f"{myRow[column_headers[TITLE_COLUMN]]}"
            mySubTitle = f"{myRow[column_headers[SUBTITLE_COLUMN]]}"
            myArg = f"{myRow[column_headers[ARG_COLUMN]]}"

        
        if is_valid_url(myArg):
            URL_CHECK = 'yes'
        else:
            URL_CHECK = 'no'
            
        
        result["items"].append({
                "title": myTitle,
                'subtitle': mySubTitle ,
                'valid': True,
                "variables": {
                    "URL_CHECK": URL_CHECK
                        },
                
                "icon": {
                    "path": 'icon.png'
                },
                'arg': myArg 
                    }) 
    print (json.dumps(result))  


def main ():
        
    fetchValues(MY_URL)



if __name__ == '__main__':
    main ()


