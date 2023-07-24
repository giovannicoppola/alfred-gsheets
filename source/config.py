#!/usr/bin/env python3

import os
import sys

def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)


ALFRED_PREFS = os.getenv('alfred_preferences')
ALFRED_WORKFLOW_DIR = f'{ALFRED_PREFS}/workflows'







    