### entering values into a google sheet using a python script (which I can then launch from Alfred)
### Saturday, June 5, 2021, 8:32 PM
# Overcast ☁️   🌡️+40°F (feels +34°F, 55%) 🌬️↘6mph 🌗&m Wed Jan  3 18:13:05 2024
# W1Q1 – 3 ➡️ 362 – 237 ❇️ 128
 




import sys
import gspread
import gspread.exceptions
import re
from oauth2client.service_account import ServiceAccountCredentials
import json
from google.oauth2 import service_account
from urllib.parse import urlparse
from config import HEADER_ROW, MY_SHEET,MY_URL, TITLE_COLUMN, SUBTITLE_COLUMN, ARG_COLUMN, COL_LIST, LAYOUT_LIST,KEYFILE, log





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


def replace_fields(original_string, series_list,column_headers):
    # Find all occurrences of "[index]" in the original string
    placeholders = [int(index) for index in re.findall(r'\[(\d+)\]', original_string)]
    
    # Replace each placeholder with the corresponding value from the series_list
    replaced_string = original_string
    for index in placeholders:
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
    
    # opening the file
    try:
        sheet = file.open_by_url(spreadsheet_url)
    
    except gspread.exceptions.NoValidUrlKeyFound as e:
        printError ("URL not valid")
    except ValueError as e:
        printError ("ValueError")
    except IOError as e:
    # Handle input/output errors
        printError ("IOError")
    except Exception as e:
    # Catch any remaining errors
        printError ("Exception")

    
    # fetching the worksheet
    try:
        worksheet = sheet.worksheet(MY_SHEET) 
    
    except gspread.exceptions.WorksheetNotFound as e:
        printError ("Sheet Not Found")


    # Get all values from the worksheet
    all_values = worksheet.get_all_values()
    

    # Extract column headers 
    column_headers = all_values[HEADER_ROW]
    #log (column_headers)
    SHEET_NCOL = len (column_headers)
    if (all(num <= SHEET_NCOL-1 for num in COL_LIST)) is False:
        myError =  f"at least one of the column numbers {[x + 1 for x in COL_LIST]} is greater than the number of columns ({SHEET_NCOL})"
        log (myError)
        printError ("check the column numbers (or the header row) in configuration",myError)
    

    
    # Create a list to store dictionaries representing each row
    rows_as_list_of_dictionaries = []

       # Iterate through each row (excluding the header row) and create a dictionary
    for row in all_values[HEADER_ROW+1:]:
        row_dict = {}
        for column_number in COL_LIST:
            
            column_name = column_headers[column_number]
            row_dict[column_name] = row[column_number]
        rows_as_list_of_dictionaries.append(row_dict)

    #log (rows_as_list_of_dictionaries)
    #log (LAYOUT_LIST)
    
    for myRow in rows_as_list_of_dictionaries:
        
        if LAYOUT_LIST:
            myTitle = replace_fields(LAYOUT_LIST[0],myRow,column_headers)
            if len(LAYOUT_LIST)>1:
                mySubTitle = replace_fields(LAYOUT_LIST[1],myRow,column_headers)
            else: 
                mySubTitle = ""
            if len(LAYOUT_LIST)>2:
                myArg = replace_fields(LAYOUT_LIST[2],myRow,column_headers)
            else: 
                myArg = ""
        
        else:
            myTitle = f"{myRow[column_headers[TITLE_COLUMN]]}"
            if SUBTITLE_COLUMN:
                mySubTitle = f"{myRow[column_headers[SUBTITLE_COLUMN]]}"
            else: 
                mySubTitle = ""
            if ARG_COLUMN:
                myArg = f"{myRow[column_headers[ARG_COLUMN]]}"
            else: 
                myArg = ""
        
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



