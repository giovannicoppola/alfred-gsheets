#!/usr/local/bin/python3
# encoding: utf-8

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



#myValue = sys.argv[2]
mySource = sys.argv[1]

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)


def addValue (myValue,mySource):
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("burattinaio-105c8840e188.json", scopes) 
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
    fetchValues ([1,2,3,4])
    #fetchValuesPublic ([1,2,3])
    
    # # The URL of the public Google Sheet
    # spreadsheet_url = "https://docs.google.com/spreadsheets/d/1mnPLSFNf_t9-C4DOYxnVXIDU_G0hXDRf8kP2wLlkB8I/edit?pli=1#gid=0"

    # # Access the public Google Sheet and print the data
    # sheet_data = access_public_google_sheet(spreadsheet_url)

    # if sheet_data is not None:
    #     log(sheet_data)



if __name__ == '__main__':
    main ()



"""
def download_column(sheet_name, column_name):
    # Your Google Sheets API credentials JSON file path
    credentials_file = 'path/to/your/credentials.json'

    # Scope for accessing Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # Authenticate with Google Sheets API
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)

    # Open the specified Google Sheet
    sheet = client.open(sheet_name)

    # Select the first worksheet (index 0) or specify a specific worksheet by title.
    worksheet = sheet.get_worksheet(0)

    # Get the values from the specified column
    column = worksheet.col_values(ord(column_name.upper()) - 64)  # Converts column letter to number (A=1, B=2, ..., Z=26)

    return column

# Replace 'Your_Sheet_Name' with the name of your Google Sheet and 'A' with the column letter you want to download.
column_data = download_column('Your_Sheet_Name', 'A')
print(column_data)


"""