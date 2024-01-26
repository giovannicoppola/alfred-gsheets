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
    for row in rows:
        extracted_strings.extend(re.findall(pattern, row))
    
    return extracted_strings


"""
TO REVIEW
import re

def extract_integer_in_square_brackets(input_string):
    # Define the regular expression pattern
    pattern = r'\[(\d+)\]'

    # Use re.search to find the pattern in the input string
    match = re.search(pattern, input_string)

    if match:
        # Extract the integer from the matched group
        extracted_integer = int(match.group(1))
        return extracted_integer
    else:
        # Return None if no match is found
        return None

# Example usage:
input_string_1 = "This is a string with [123] inside."
result_1 = extract_integer_in_square_brackets(input_string_1)
print(result_1)  # Output: 123

input_string_2 = "No integer in this string."
result_2 = extract_integer_in_square_brackets(input_string_2)
print(result_2)  # Output: None

"""

ALFRED_PREFS = os.getenv('alfred_preferences')
ALFRED_WORKFLOW_DIR = f'{ALFRED_PREFS}/workflows'

MY_URL = os.path.expanduser(os.getenv('MY_URL', ''))
KEYFILE = os.path.expanduser(os.getenv('KEYFILE', ''))
MY_SHEET = os.path.expanduser(os.getenv('MY_SHEET', ''))

HEADER_ROW = int(os.path.expanduser(os.getenv('HEADER_ROW', ''))) - 1


TITLE_COLUMN = int(os.path.expanduser(os.getenv('TITLE_COLUMN', '')))-1
SUBTITLE_COLUMN = int(os.path.expanduser(os.getenv('SUBTITLE_COLUMN', '')))-1
APPEND_COLUMN = int(os.path.expanduser(os.getenv('APPEND_COLUMN', '')))

ARG_COLUMN_V = os.path.expanduser(os.getenv('ARG_COLUMN', ''))
if ARG_COLUMN_V:
    ARG_COLUMN = int(ARG_COLUMN_V)-1
else:
    ARG_COLUMN = 0
    

MY_LAYOUT = os.path.expanduser(os.getenv('MY_LAYOUT', ''))

if not MY_LAYOUT:
    log ("layout empty")
else:
    log ("layout present")


    
LAYOUT_LIST = extract_quoted_strings(MY_LAYOUT)

log (LAYOUT_LIST)


    