from numpy import ndarray
from DataType import DataType
from Part import Part


class PartLabel(Part):
    def __init__(self, identifier: str, dataType: DataType, layer: str, reference: ndarray, text1, text2):
        super().__init__(identifier, dataType, layer, None, reference, None)
        
        self.text1 = text1
        self.text2 = text2

    