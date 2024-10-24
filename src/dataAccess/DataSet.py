from packaging.version import Version
from dataAccess import DataLayer


def create_data_set(data):
    scheme_version = Version("0.0")
    
    if data[0][0].startswith('Scheme-Version'):
        scheme_version_entry = data[0][0]
        scheme_version_text = scheme_version_entry.split('=')[1]
        scheme_version = Version(scheme_version_text.strip())
        
    
    for i in range(1,len(data)): # Skip first line
        pass

    return data_set


class DataSet:
    def __init__(dl:DataLayer):
        dataSet = []