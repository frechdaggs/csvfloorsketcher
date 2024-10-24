from datetime import date
import re
from typing import List, cast
import numpy as np
from ConsolePrinter import print_info
from exceptions.InputError import InputError
from Part import Part
from DataType import DataType
from PartLabel import PartLabel

class ConstructionPlanSet:
    def __init__(self):
        self.part_list:List[Part] = list()
        self.meta_information:dict[str, str] = {'Date': date.today().strftime("%d.%m.%Y")}
        self.settings:dict[str, str] = {'PageSize': 'A4'}
    
    def parse_and_calculate_point(self, expression:str, layer, reference:np.ndarray = None):
        points = expression.split('+')
        
        parsed_points = []
        
        for point in points:
            tokens = re.findall(r"\((.*?)\)", point)
            
            if (len(tokens) != 1):
                raise ImportError(f'Unable to intepret point: {point}')
            
            point = tokens[0]
            
            if (',' in point):
                x_str, y_str = point.split(',')
                x, y = int(x_str), int(y_str)
            else:
                x, y = self.get_coordinates_of_point(point, layer)

                if (reference is not None):
                    x -= reference[0]
                    y -= reference[1]
            
            parsed_points.append(tuple([x, y]))

        result_x = 0
        result_y = 0
        for parsed_point in parsed_points:
            result_x += parsed_point[0]
            result_y += parsed_point[1]
            
        return np.array([result_x, result_y])

    def add_data(self, date):
        print_info(f'Adding data: {date}')

        identifier: str = date['Identifier']
        layer: str = date['Layer']
        dimOffset: str = date['DimOffset']
        reference_expression: str = date['Reference']

        try:
            dataType: DataType = DataType[date['Type']]
        except KeyError:
            raise InputError(f'Unknown Type: {date['Type']}')

        payload = date['Payload']
        
        reference:np.ndarray = None
        if reference_expression != '':
            reference = self.parse_and_calculate_point(reference_expression, layer)

        match dataType:
            case DataType.MetaInformation:
                self.meta_information[identifier] = payload[0]
            case DataType.Settings:
                self.settings[identifier] = payload[0]
            case DataType.Label:
                self.check_payload_length(payload, 1)
                text1 = payload[0]
                text2 = '' if len(payload) <= 1 else payload[1]
                self.part_list.append(PartLabel(identifier, dataType, layer, reference, text1, text2))
            case _:
                payload_contains_relative_points:bool = dataType not in (DataType.XDim, DataType.XDimC, DataType.YDim, DataType.YDimC)
                
                calculation_reference = None
                if payload_contains_relative_points:
                    calculation_reference = reference
                
                points = list(map(lambda n: self.parse_and_calculate_point(n, layer, calculation_reference),payload))
                self.part_list.append(Part(identifier, dataType, layer, dimOffset, reference, points))

    def check_payload_length(self, payload, min_length):
        if len(payload) < min_length:
            raise InputError(f'Payload must have at least {min_length} entr(y/ies)')


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

        referenced_part:Part = self.get_part(identifier, layer)

        if (idx < 0):
            raise InputError(f"Error parsing {expression}: Referencing index must be greater then 0")
        
        referenced_point = referenced_part.points[idx]

        x, y = referenced_point[0]+referenced_part.reference[0], referenced_point[1]+referenced_part.reference[1]

        return x, y

    def get_parts_in_layer(self, layer) -> List[Part]:
        return list(filter(lambda n: n.layer == layer, self.part_list))
    
    def get_layers(self):
        return set(map(lambda n: n.layer, self.part_list))

