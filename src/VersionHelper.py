import os
import re
import sys

def get_version():
    version_path = resource_path('version.txt')
    
    with open(version_path) as f:
        content = f.read()
        tokens = re.findall(r"(\d+)\.(\d+)\.(\d+)\.(\d+)", content)
  		
    return int(tokens[0][0]), int(tokens[0][1]), int(tokens[0][2]), int(tokens[0][3])

def version_to_str(major:int, minor:int, patch:int, rev:int):
    return f'{major:02d}.{minor:03d}.{patch:02d}.{rev:02d}'

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

    return os.path.join(base_path, relative_path)

