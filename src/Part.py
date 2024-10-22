from DataType import DataType
from Exceptions.InputError import InputError


class Part:
    def __init__(self, identifier:str, dataType:DataType, layer:str, dimOffset:str, reference, points):
        self.identifier = identifier
        self.dataType = dataType
        self.layer = layer
        
        try:
            self.dimOffset:float = 0 if dimOffset=='' else float(dimOffset)
        except ValueError:
            raise InputError(f'Value with key "Dim-Offset" must be a floating number.')
        
        self.reference = reference
        self.points = points