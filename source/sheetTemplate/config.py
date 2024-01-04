#!/usr/bin/env python3

import os
import sys
import re

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)


ALFRED_PREFS = os.getenv('alfred_preferences')
ALFRED_WORKFLOW_DIR = f'{ALFRED_PREFS}/workflows'

MY_URL = os.path.expanduser(os.getenv('MY_URL', ''))
MY_SHEET = os.path.expanduser(os.getenv('MY_SHEET', ''))

HEADER_ROW = int(os.path.expanduser(os.getenv('HEADER_ROW', ''))) - 1


TITLE_COLUMN = int(os.path.expanduser(os.getenv('TITLE_COLUMN', '')))-1
SUBTITLE_COLUMN = int(os.path.expanduser(os.getenv('SUBTITLE_COLUMN', '')))-1

ARG_COLUMN_V = os.path.expanduser(os.getenv('ARG_COLUMN', ''))
if ARG_COLUMN_V:
    ARG_COLUMN = int(ARG_COLUMN_V)-1
else:
    ARG_COLUMN = 0
    

MY_LAYOUT = os.path.expanduser(os.getenv('MY_LAYOUT', ''))


# def extract_quoted_strings(string):
#     pattern = r'"((?:[^"]|"[^"]*")*)"'  # Matches text within double quotes
#     extracted_strings = re.findall(pattern, string)
#     return extracted_strings

def extract_quoted_strings(string):
    # Split the input string into rows (assuming rows are separated by newline character '\n')
    rows = string.split('\n')
    
    # Apply the regex pattern to each row and extend the result list
    pattern = r'"((?:[^"]|"[^"]*")*)"'
    extracted_strings = []
    for row in rows:
        extracted_strings.extend(re.findall(pattern, row))
    
    return extracted_strings
    
LAYOUT_LIST = extract_quoted_strings(MY_LAYOUT)

log (LAYOUT_LIST)

# if MY_LAYOUT:
    
#     MY_LAYOUT_S = re.sub(r'\[(\d+)\]', r'myRow[column_headers[{}]]', MY_LAYOUT)
#     my_numbers = re.findall(r'\[(\d+)\]', MY_LAYOUT)
#     my_numbers = [int(num) for num in my_numbers]  # Convert strings to integers
    
# else:
#     MY_LAYOUT_S = '' 
    



    