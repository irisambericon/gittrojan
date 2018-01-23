#!/usr/bin/python
import os

def run(**args):
    print "[*] in environment module."
    return str(os.environ)
