import argparse
import os
from CSVLoader import CSVLoader
from ConsolePrinter import print_error, print_info
from ConstructionPlanSet import ConstructionPlanSet
from ConstructionPlanWriter import ConstructionPlanWriter
from Exceptions.InputError import InputError


def read_data(csv_file):
    cSVLader = CSVLoader(csv_file)
    return cSVLader.load()

def parse_data(data):
    data_dict = []
    for i in range(1,len(data)): # Skip first line
        date = data[i]
        if date:
            if date[2] == '':
                print_info(f'Skipping data because the type is not specified - line: {i} - {date}')
                continue

            print_info(f'Parsing data - line: {i} - {date}')

            payload = date[5:len(date)]
            payload = list(filter(lambda n: n!='', payload))
            data_dict.append(
                {
                    'Identifier':date[0],
                    'Layer':date[1],
                    'Type':date[2],
                    'DimOffset':date[3],
                    'Reference':date[4],
                    'Payload':payload
                })
        
    return data_dict

def main():
    parser = argparse.ArgumentParser(description="Erzeugt einen Bauplan auf Basis einer Bemaßungstabelle.")

    parser.add_argument('daten', type=str, help='Pfad der Bemaßungstabelle')
    parser.add_argument('--debug', action="store_true", help='Erweitert die Zeichnung um Informationen, die die Arbeit mit der Zeichnung erleichtern.')
    
    args = parser.parse_args()
    
    csv_file = args.daten
    debug_mode = args.debug

    file_path_without_ext, ext = os.path.splitext(csv_file)
    out_pdf_file = file_path_without_ext + ".pdf"
    out_svg_file = file_path_without_ext + ".svg"

    data = read_data(csv_file)

    data_dict = parse_data(data)

    constructionPlanSet = ConstructionPlanSet()
    
    for date in data_dict:
        constructionPlanSet.add_data(date)

    constructionPlanWriter = ConstructionPlanWriter(file_path_without_ext, constructionPlanSet, debug_mode)
    constructionPlanWriter.write()


if __name__ == '__main__':
    try:
        main()
    except InputError as e: print_error(e)
        
        
    


