import os

def get_module_name():
    fullpath = os.path.abspath(__file__)
    return fullpath.split('/')[-1]
