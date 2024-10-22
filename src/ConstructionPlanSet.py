from datetime import date
import re
from typing import List, cast
import numpy as np
from ConsolePrinter import print_info
from Exceptions.InputError import InputError
from Part import Part
from DataType import DataType

class ConstructionPlanSet:

    def __init__(self):
        self.part_list:List[Part] = list()
        self.meta_information:dict[str, str] = {'Date': date.today().strftime("%d.%m.%Y")}
        self.settings:dict[str, str] = {'PageSize': 'A4'}


    def parse_and_calculate_point(self, expression:str, layer):
        tokens = re.findall(r"\((.*?)\)", expression)

        result_x = 0
        result_y = 0

        for token in tokens:
            if (',' in token):
                x_str, y_str = token.split(',')
                x, y = int(x_str), int(y_str)
            else:
                x, y = self.get_coordinates_of_point(token, layer)

            result_x += x
            result_y += y


        return np.array([result_x, result_y])
    

    def add_data(self, date):
        print_info(f'Adding data: {date}')

        identifier: str = date['Identifier']
        layer: str = date['Layer']
        dimOffset: str = date['DimOffset']
        reference: str = date['Reference']
        dataType: DataType = DataType[date['Type']]
        payload = date['Payload']

        if (dataType == DataType.MetaInformation):
            self.meta_information[identifier] = payload[0]
        elif (dataType == DataType.Settings):
            self.settings[identifier] = payload[0]
        else:
            points = list(map(lambda n: self.parse_and_calculate_point(n, layer),payload))
            self.part_list.append(Part(identifier, dataType, layer, dimOffset, self.parse_and_calculate_point(reference, layer), points))

    def get_part(self, identifier, layer):
        parts = list(filter(lambda n: n.identifier == identifier and n.layer == layer, self.part_list))
        if (len(parts) > 1):
            raise InputError(f'There are more then one {Part.__name__} with identifier "{identifier}" in layer "{layer}"')
        elif (len(parts) < 1):
            raise InputError(f'Cant find any {Part.__name__} with identifier "{identifier}" in layer "{layer}"')
        else:
            return parts[0]


    def get_coordinates_of_point(self, expression, layer):
        tokens = re.findall(r"(.+)-(\d+)", expression)
        identifier = tokens[0][0]
        idx = int(tokens[0][1])-1

        part:Part = self.get_part(identifier, layer)

        if (idx < 0):
            raise InputError(f"Error parsing {expression}: Referencing index must be greater then 0")
        
        point = part.points[idx]

        return point[0]+part.reference[0], point[1]+part.reference[1]

    def get_parts_in_layer(self, layer):
        return list(filter(lambda n: n.layer == layer, self.part_list))
    
    def get_layers(self):
        return set(map(lambda n: n.layer, self.part_list))

