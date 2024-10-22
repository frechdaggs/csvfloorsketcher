from typing import List
import numpy as np


def gen_line_string(pt1:np.ndarray, pt2:np.ndarray, class_name:str = None, adds:str = None):
    string = '<line '
    if class_name:
        string += f'class="{class_name}" '
    if adds:
        string += f'{adds} '
    string += f'x1="{pt1[0]}" '
    string += f'y1="{pt1[1]}" '
    string += f'x2="{pt2[0]}" '
    string += f'y2="{pt2[1]}" '
    string += f'/>'

    return string

def gen_path_string(pts:List[np.ndarray], is_closed_path:bool, class_name:str = None, adds:str = None):
    string = '<path '
    if class_name:
        string += f'class="{class_name}" '
    if adds:
        string += f'{adds} '
    
    sub_string = ''
    for i in range(0,len(pts)):
        if i == 0:
            sub_string += 'M'
        else:
            sub_string += ' L'
        
        pt = pts[i]
        sub_string += f'{pt[0]} {pt[1]}'

    if is_closed_path:
        sub_string += ' Z'

    string += f'd="{sub_string}" '
    string += f'/>'

    return string