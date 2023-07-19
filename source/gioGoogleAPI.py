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

