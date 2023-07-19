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


myValue = sys.argv[2]
mySource = sys.argv[1]


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


""" from chatGPT in case I want to try with a google doc too:
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

# Replace with the appropriate values
DOCUMENT_ID = 'your-document-id'
APPEND_TEXT = 'your-text-to-append'

def append_to_document():
    # Get credentials
    credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/drive'])

    # Build the Drive API client
    drive_service = build('drive', 'v3', credentials=credentials)

    # Build the Docs API client
    docs_service = build('docs', 'v1', credentials=credentials)

    # Get the document body
    result = drive_service.files().get(fileId=DOCUMENT_ID, fields='*').execute()
    doc_body = result.get('body')

    # Find the last paragraph
    last_paragraph = None
    for i, element in enumerate(doc_body.get('content')):
        if element.get('paragraph') is not None:
            last_paragraph = i

    # Append the text to the last paragraph
    if last_paragraph is not None:
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': doc_body.get('content')[last_paragraph].get('endIndex') - 1
                    },
                    'text': '\n' + APPEND_TEXT
                }
            }
        ]
        docs_service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

if __name__ == '__main__':
    try:
        append_to_document()
    except HttpError as error:
        print(f'An error occurred: {error}')


"""