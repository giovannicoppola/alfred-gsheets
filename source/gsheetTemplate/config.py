import os
import sys
import re

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)

def extract_quoted_strings(string):
    """
    A function to process the custom layout and check that all the needed fields are included
    """
    # Split the input string into rows (assuming rows are separated by newline character '\n')
    rows = string.split('\n')
    
    # Apply the regex pattern to each row and extend the result list
    pattern = r'"((?:[^"]|"[^"]*")*)"'
    extracted_strings = []
    extracted_integers = []
    pattern_col = r'\[(\d+)\]'
    for row in rows:
        extracted_strings.extend(re.findall(pattern, row))
        # Use re.search to find the pattern in the input string
        matches = re.findall(pattern_col, row)
        extracted_integers.extend ([int(match)-1 for match in matches])
            
    return extracted_strings, list(set(extracted_integers))


"""
        extracted_integer = int(match.group(1))
        return extracted_integer

"""

ALFRED_PREFS = os.getenv('alfred_preferences')
ALFRED_WORKFLOW_DIR = f'{ALFRED_PREFS}/workflows'

MY_URL = os.path.expanduser(os.getenv('MY_URL', ''))
KEYFILE = os.path.expanduser(os.getenv('KEYFILE', ''))
MY_SHEET = os.path.expanduser(os.getenv('MY_SHEET', ''))

HEADER_ROW = int(os.path.expanduser(os.getenv('HEADER_ROW', ''))) - 1


TITLE_COLUMN = int(os.path.expanduser(os.getenv('TITLE_COLUMN', '')))-1
SUBTITLE_COLUMN = os.path.expanduser(os.getenv('SUBTITLE_COLUMN', ''))
ARG_COLUMN = os.path.expanduser(os.getenv('ARG_COLUMN', ''))

MY_LAYOUT = os.path.expanduser(os.getenv('MY_LAYOUT', ''))
LAYOUT_LIST = ''
if not MY_LAYOUT:
    log ("layout empty")
    COL_LIST = [TITLE_COLUMN]

    
    if SUBTITLE_COLUMN:
        SUBTITLE_COLUMN = int(os.path.expanduser(os.getenv('SUBTITLE_COLUMN', '')))-1
        COL_LIST.append (SUBTITLE_COLUMN)

    
    if ARG_COLUMN:
        ARG_COLUMN = int(ARG_COLUMN)-1
        COL_LIST.append (ARG_COLUMN)

else:
    LAYOUT_LIST, COL_LIST = extract_quoted_strings(MY_LAYOUT)
    #log (LAYOUT_LIST)
    
 
APPEND_COLUMN = os.path.expanduser(os.getenv('APPEND_COLUMN', ''))
#log (COL_LIST)






    