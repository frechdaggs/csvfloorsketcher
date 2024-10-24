from abc import ABC, abstractmethod
from io import BytesIO
import math
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3
from svglib.svglib import svg2rlg
from typing import Dict, List, cast
import numpy as np
from ConstructionPlanSet import ConstructionPlanSet
from Exceptions.InputError import InputError
from Exceptions.NotImplementedException import NotImplementedException
from Part import Part
from DataType import DataType
from PartLabel import PartLabel
import SVGHelper
from VersionHelper import get_version, version_to_str


class ConstructionPlanWriter:
    plan_margin = 50

    def __init__(self, file_path_base, constructionPlanSet:ConstructionPlanSet, debug_mode):
        self.file_path_base = file_path_base
        self.constructionPlanSet = constructionPlanSet
        self.debug_mode = debug_mode
        self.scale_divisor = int(constructionPlanSet.settings['ScaleDivisor'])

        match constructionPlanSet.settings['PageSize']:
            case 'A4':
                self.pagesize = A4
                self.pdf_width, self.pdf_height = 21, 29.7
            case 'A3':
                self.pagesize = A3
                self.pdf_width, self.pdf_height = 29.7, 42
            case _:
                raise ValueError(f'Page size {constructionPlanSet.settings['PageSize']} is not supported')
        
        self.svg_width = ConstructionPlanWriter.cm_to_dots(self.pdf_width)
        self.svg_height = ConstructionPlanWriter.cm_to_dots(self.pdf_height)


    def cm_to_dots(value):
        dpi = 72
        cm_per_inch = 2.54

        return value*dpi/cm_per_inch

    def write(self, is_savig_svg:bool):
        cps = self.constructionPlanSet

        layers = sorted(cps.get_layers())

        cps.meta_information['Massstab'] = f'1 : {self.scale_divisor}'
        
        pdf_buffer = BytesIO()
        pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=self.pagesize)
        for layer in layers:
            cps.meta_information['Ebene'] = layer

            svg_content = self.make_svg_content(cps, layer)
            
            svg_buffer = BytesIO(svg_content.encode('utf-8'))
            
            drawing = svg2rlg(svg_buffer)
            renderPDF.draw(drawing, pdf_canvas, 0, 0)
            pdf_canvas.showPage()

            if is_savig_svg:
                self.save_svg(layer, svg_buffer)            

        pdf_canvas.save()
        
        pdf_file_path = f'{self.file_path_base}.pdf'
        pdf_buffer.seek(0)
        with open(pdf_file_path, 'wb') as f:
            f.write(pdf_buffer.read())

    def save_svg(self, layer, svg_buffer):
        svg_file_path = f'{self.file_path_base}_{layer}.svg'
        svg_buffer.seek(0)
            
        with open(svg_file_path, 'wb') as svg_file:
            svg_file.write(svg_buffer.read())

    def make_svg_content(self, cps, layer):
        svg_content = ''
        svg_content += self.make_header(self.svg_width, self.svg_height)
        plan_border_content, meta_inforamtion_height = self.make_plan_border(self.svg_width, self.svg_height, self.plan_margin, cps.meta_information)
        svg_content += plan_border_content

        svg_content += self.make_compass(self.svg_width, self.svg_height, self.plan_margin, cps.settings['CompassRotation'])

        if self.debug_mode:
            anchor = np.array([self.plan_margin + 10, self.svg_height - self.plan_margin - meta_inforamtion_height - 10])
            svg_content += self.make_axes(anchor)

        body_heigth = self.svg_height - meta_inforamtion_height
        svg_content += self.make_body(self.svg_width, body_heigth, layer)

        svg_content += self.make_footer()
        return svg_content

    def make_header(self, svg_width, svg_height):
        header_content = ''
        header_content += f'<svg width="{svg_width}" height="{svg_height}" xmls="http://www.x3.org/2000/svg">\n'
        header_content += '<style>\n'
        header_content += self.make_style('plan-boarder', 'fill: none', 'stroke: black', 'stroke-width: 2px')
        header_content += self.make_style('watermark-text', 'font-size: 8pt', 'font-family: monospace')
        header_content += self.make_style('meta-information-key', 'font-size: 10pt', 'font-family: monospace', 'text-anchor: start')
        header_content += self.make_style('meta-information-text', 'font-size: 10pt', 'font-family: monospace', 'font-weight: bold', 'text-anchor: middle')
        header_content += self.make_style('label-text', 'fill: black', 'font-size: 10pt', 'font-family: monospace', 'font-weight: bold')
        header_content += self.make_style('debug-text', 'fill: #ac9d00', 'font-size: 10pt', 'font-family: monospace', 'font-weight: bold')
        header_content += self.make_style('debug-line', 'fill: none', 'stroke: #ac9d00', 'stroke-width: 0.5px')
        header_content += self.make_style('dim-text', 'fill: #a10000', 'font-size: 3mm', 'font-family: monospace', 'font-weight: bold', 'text-anchor: middle')
        header_content += self.make_style('dim-line', 'fill: none', 'stroke: black', 'stroke-width: 0.5px')
        header_content += self.make_style('outline', 'fill: #2b2b2b', 'stroke: black', 'stroke-width: 1px')
        header_content += self.make_style('room', 'fill: #d9d9d9', 'stroke: black', 'stroke-width: 1px')
        header_content += self.make_style('stairs', 'fill: #b3b3b3', 'stroke: black', 'stroke-width: 1px')
        header_content += self.make_style('steps', 'fill: none', 'stroke: black', 'stroke-width: 1px')
        header_content += self.make_style('room-connection', 'fill: #797979', 'stroke: black', 'stroke-width: 1px')
        header_content += self.make_style('opening-arc', 'fill: #b3b3b3', 'stroke: black', 'stroke-width: 0.5px')
        header_content += '</style>\n'
        return header_content

    def make_plan_border(self, svg_width, svg_height, margin, meta_information:dict[str, str]):
        plan_border_width = svg_width-margin*2
        plan_border_heigth = svg_height-margin*2
    	
        plan_border_content = ''
        plan_border_content += f'<rect class="plan-boarder" width="{plan_border_width}" height="{plan_border_heigth}" x="{margin}" y="{margin}" />\n'
        
        maj, min, patch, rev = get_version()
        version_str=version_to_str(maj, min, patch, rev)

        watermark_text_1 = f'Created with CSV Floor Sketcher v{version_str}'
        watermark_text_2 = '(https://github.com/frechdaggs/csvfloorsketcher)'
        plan_border_content += f'<text class="watermark-text" x="{margin}" y="{margin + plan_border_heigth + 10}">{watermark_text_1}<tspan x="{margin}" dy="10">{watermark_text_2}</tspan></text>\n'

        info_box_width = plan_border_width/3
        info_box_height = 50
        info_box_margin = 5
        info_box_key_y_offset = 10
        info_box_text_y_offset = -5

        counter:int = -1
        for key in meta_information:
            counter += 1

            info_box_x = plan_border_width + margin - info_box_width * (counter%2 + 1)
            info_box_y = plan_border_heigth + margin - info_box_height * (int(counter/2) + 1)

            plan_border_content += f'<rect class="plan-boarder" width="{info_box_width}" height="{info_box_height}" x="{info_box_x}" y="{info_box_y}" />\n'
            plan_border_content += f'<text class="meta-information-key" x="{info_box_x+info_box_margin}" y="{info_box_y+info_box_margin+info_box_key_y_offset}">{key}</text>\n'
            plan_border_content += f'<text class="meta-information-text" x="{info_box_x + info_box_width/2}" y="{info_box_y + info_box_height - info_box_margin + info_box_text_y_offset}">{meta_information[key]}</text>\n'
            

        return plan_border_content, info_box_height * (int(counter/2) + 1)

    def make_axes(self, anchor:np.ndarray):
        anchor1 = anchor + np.array([0, -50])
        anchor2 = anchor
        anchor3 = anchor + np.array([50, 0])
        axes_content = ''
        axes_content += f'<path class="debug-line" d="M{anchor1[0]} {anchor1[1]} L{anchor2[0]} {anchor2[1]} L{anchor3[0]} {anchor3[1]}" />\n'
        axes_content += f'<text class="debug-text" text-anchor="end" x="{anchor3[0]}" y="{anchor3[1] - 5}">x</text>\n'
        axes_content += f'<text class="debug-text" x="{anchor1[0] + 5}" y="{anchor1[1] + 5}">y</text>'

        return axes_content

    def make_compass(self, svg_width, svg_height, margin, compass_rotation):
        
        compass_content = ''
        compass_content += f'<g transform="translate({margin+80} {svg_height-margin-80})">\n'
        compass_content += f'<g transform="rotate({compass_rotation} 0 0)">\n'
        compass_content += f'<circle r="50" stroke="black" stroke-width="2" fill="none" />\n'
        compass_content += f'<circle r="25" stroke="black" stroke-width="2" fill="none" />\n'
        compass_content += f'<circle r="2" stroke="black" stroke-width="2" fill="black" />\n'
        compass_content += f'<line y1="-25" y2="25" stroke="black" stroke-width="2" />\n'
        compass_content += f'<text x="0" y="-30" font-family="monospace" font-size="20" text-anchor="middle" fill="black">N</text>\n'
        compass_content += f'<text x="0" y="45" font-family="monospace" font-size="20" text-anchor="middle" fill="black">S</text>\n'
        compass_content += f'<text x="-40" y="7" font-family="monospace" font-size="20" text-anchor="middle" fill="black">W</text>\n'
        compass_content += f'<text x="40" y="7" font-family="monospace" font-size="20" text-anchor="middle" fill="black">E</text>\n'
        compass_content += '</g></g>\n'

        return compass_content

    def make_footer(self):
        return '</svg>'

    def make_style(self, class_name, *argv):
        style_content = ''
        style_content += f'.{class_name} {{\n'
        
        for arg in argv:
            style_content += f'{arg};\n'

        style_content += '}\n'
        return style_content


    def get_style_class(self, dataType:DataType):
        match dataType:
            case DataType.Outline:
                return 'outline'
            case DataType.Room:
                return 'room'
            case DataType.Stairs:
                return 'stairs'
            case DataType.Steps:
                return 'steps'
            case DataType.RoomConnection:
                return 'room-connection'
            case DataType.OpeningArc:
                return 'opening-arc'
            case DataType.XDim|DataType.YDim|DataType.XDimC|DataType.YDimC:
                return 'dim'
            case DataType.Label:
                return 'label-text'
            case _:
                raise InputError(f'No style class implemented for Part with type {dataType}')


    def make_debug_information(self, layer:str, canvas_left_limit, canvas_right_limit):
        part_list = self.constructionPlanSet.get_parts_in_layer(layer)

        debug_content = ''

        counter = 0
        for part in sorted(part_list, key=lambda n: n.dataType.value):
            match part.dataType:
                case DataType.Outline | DataType.Room | DataType.RoomConnection | DataType.OpeningArc:
                    ref_id_text_pos = np.array([canvas_right_limit, -counter*15])
                    shape = DebugReferenceInformationShape(self.scale_divisor, part, ref_id_text_pos)
                    
                    debug_content += f'{shape.get_svg_string('debug')}\n'

                    counter += 1
        
        debug_content += f'path class\n'

        return debug_content

    def make_body(self, body_width, body_heigth, layer):
        part_list = self.constructionPlanSet.get_parts_in_layer(layer)
        
        body_content = ''
        shapes = list()

        x_min = math.inf
        x_max = -math.inf
        y_min = math.inf
        y_max = -math.inf

        for part in sorted(part_list, key=lambda n: n.dataType.value):
            match part.dataType:
                case DataType.Outline | DataType.Room | DataType.Stairs | DataType.RoomConnection:
                    shape = PathShape(self.scale_divisor, part.points, part.reference)

                    x_min_shape, x_max_shape, y_min_shape, y_max_shape = shape.get_boundry()
                    if (x_min_shape < x_min): x_min = x_min_shape
                    if (x_max_shape > x_max): x_max = x_max_shape
                    if (y_min_shape < y_min): y_min = y_min_shape
                    if (y_max_shape > y_max): y_max = y_max_shape

                    shapes.append(shape.get_svg_string(self.get_style_class(part.dataType)))

                case DataType.Steps:
                    shape = StepsShape(self.scale_divisor, part.points, part.reference)

                    shapes.append(shape.get_svg_string(self.get_style_class(part.dataType)))

                case DataType.OpeningArc:
                    shape = OpeningArgShape(self.scale_divisor, part.points, part.reference)
                    shapes.append(shape.get_svg_string(self.get_style_class(part.dataType)))
                    
                case DataType.XDim | DataType.YDim | DataType.XDimC | DataType.YDimC:
                    pt1 = part.points[0]
                    pt2 = part.points[1]

                    shapes.append(DimShape(self.scale_divisor, part.dataType, pt1, pt2, part.dimOffset, part.reference).get_svg_string(self.get_style_class(part.dataType)))

                case DataType.Label:
                    part_label = cast(PartLabel, part)
                    shapes.append(Label(self.scale_divisor, part_label).get_svg_string(self.get_style_class(part.dataType)))

                case _:
                    raise InputError(f'Part with type {part.dataType} not implemented in {ConstructionPlanWriter.__name__}')


        x_offset = body_width/2 - (x_max - x_min)/2
        y_offset = body_heigth/2 - (y_max - y_min)/2 - y_min
        body_content += f'<g transform="translate({x_offset} {y_offset})">\n'

        for shape in shapes:
            body_content += f'{shape}\n'
        
        if self.debug_mode:
            body_content += self.make_debug_information(layer, -x_offset, body_width-x_offset)


        body_content += '</g>\n'

        return body_content

class Shape(ABC):
    def __init__(self, scale_divisor):
        self.scale_divisor = scale_divisor

    @abstractmethod
    def get_svg_string(self, class_str):
        raise NotImplementedException(self.get_boundry.__name__, type(self).__name__)

    @abstractmethod
    def get_boundry(self):
        raise NotImplementedException(self.get_boundry.__name__, type(self).__name__)

    def cm_to_dots(self, value):
        return ConstructionPlanWriter.cm_to_dots(value)
    
    def invert_y(self, point:np.ndarray):
        return np.matmul(point, np.array([[1, 0], [0, -1]]))

class Label(Shape):
    def __init__(self, scale_divisor, part_label:PartLabel):
        super().__init__(scale_divisor)

        self.text_anchor = self.cm_to_dots(self.invert_y(part_label.reference))/self.scale_divisor
        self.text = f'{part_label.text1}'
        if part_label.text2 != '':
            self.text += f' ({part_label.text2})'

    def get_svg_string(self, class_str):
        return f'<text class="{class_str}" x="{self.text_anchor[0]}" y="{self.text_anchor[1]}">{self.text}</text>'

    def get_boundry(self):
        return super().get_boundry()

class RectangleShape(Shape):
    def __init__(self, scale_divisor, width, height, center):
        super().__init__(scale_divisor)
        self.width = width
        self.height = height
        self.center = self.invert_y(center)

        self.scaled_width = self.cm_to_dots(self.width)/self.scale_divisor
        self.scaled_height = self.cm_to_dots(self.height)/self.scale_divisor

        #top-left corner
        self.x = self.cm_to_dots(self.center[0])/self.scale_divisor - self.scaled_width/2
        self.y = self.cm_to_dots(self.center[1])/self.scale_divisor - self.scaled_height/2
    
    def get_svg_string(self, class_str):
        return f'<rect class="{class_str}" width="{self.scaled_width}" height="{self.scaled_height}" x="{self.x}" y="{self.y}" />'

    def get_boundry(self):
        return self.x, self.x + self.scaled_width, self.y, self.y + self.scaled_height

class DebugReferenceInformationShape(Shape):
    _svg_content = ''

    def __init__(self, scale_divisor, part:Part, ref_id_text_pos:np.ndarray):
        super().__init__(scale_divisor)
        self.part = part
        self.ref_id_text_pos = ref_id_text_pos

        points = part.points
        reference = part.reference
        
        referenced_points = list(map(lambda n: np.add(n,reference), points))
        mirrored_points = list(map(lambda n: self.invert_y(n), referenced_points))
        self.points_transformed = list(map(lambda n: self.cm_to_dots(n)/self.scale_divisor, mirrored_points))

    def get_svg_string(self, class_str):
        ref_id_line_pt1 = self.ref_id_text_pos + np.array([-70,-5])
        ref_id_line_pt2 = self.points_transformed[0]
        self._svg_content += f'<line class="{class_str}-line" x1="{ref_id_line_pt1[0]}" y1="{ref_id_line_pt1[1]}" x2="{ref_id_line_pt2[0]}" y2="{ref_id_line_pt2[1]}"/>\n'

        for i in range(0,len(self.points_transformed)):
            point = self.points_transformed[i]
            self._svg_content += f'<text class="{class_str}-text" text-anchor="middle" x="{point[0]}" y="{point[1]+5}">{i+1}</text>\n'

        self._svg_content += f'<text class="{class_str}-text" text-anchor="end" x="{self.ref_id_text_pos[0]}" y="{self.ref_id_text_pos[1]}">{self.part.identifier}</text>'

        return self._svg_content
    
    def get_boundry(self):
        return super().get_boundry()


class DimShape(Shape):
    def __init__(self, scale_divisor, dimType:DataType, pt1, pt2, dim_offset:float, reference = None):
        super().__init__(scale_divisor)
        
        if (not (dimType == DataType.XDim or dimType == DataType.YDim or dimType == DataType.XDimC or dimType == DataType.YDimC)):
            raise Exception(f'{DimShape.__name__} cant handle {DataType.__name__} other then {DataType.XDim}, {DataType.YDim}, {DataType.XDim} or {DataType.YDim}')

        self.dim_offset = dim_offset
        self.pt1_transformed = self.cm_to_dots(self.invert_y(pt1))/self.scale_divisor
        self.pt2_transformed = self.cm_to_dots(self.invert_y(pt2))/self.scale_divisor

        if reference is None:
            reference = pt1
        
        reference_transformed = self.cm_to_dots(self.invert_y(reference))/self.scale_divisor
        
        match dimType:
            case DataType.XDim|DataType.XDimC:
                self.dimension_text = abs(pt2[0]-pt1[0])
                                    
                if (dimType is DataType.XDimC):
                    self.dimension_text = f'({self.dimension_text})'

                self.dim_line_anchor1 = np.array([self.pt1_transformed[0], reference_transformed[1]])
                self.dim_line_anchor2 = np.array([self.pt2_transformed[0], reference_transformed[1]])
                
                if pt2[0]>pt1[0]:
                    self.text_offset_y = -2
                    self.dim_line_anchor1 = self.dim_line_anchor1 - np.array([0, dim_offset])
                    self.dim_line_anchor2 = self.dim_line_anchor2 - np.array([0, dim_offset])
                else:
                    self.text_offset_y = 9
                    self.dim_line_anchor1 = self.dim_line_anchor1 + np.array([0, dim_offset])
                    self.dim_line_anchor2 = self.dim_line_anchor2 + np.array([0, dim_offset])
                
                self.text_offset_x = 0
                self.text_rotation = 0

            case DataType.YDim|DataType.YDimC:
                self.dimension_text = abs(pt2[1]-pt1[1])
                
                if (dimType is DataType.YDimC):
                    self.dimension_text = f'({self.dimension_text})'
                    
                self.dim_line_anchor1 = np.array([reference_transformed[0], self.pt1_transformed[1]])
                self.dim_line_anchor2 = np.array([reference_transformed[0], self.pt2_transformed[1]])

                if pt2[1]>pt1[1]:
                    self.text_offset_x = -2
                    self.dim_line_anchor1 = self.dim_line_anchor1 - np.array([dim_offset, 0])
                    self.dim_line_anchor2 = self.dim_line_anchor2 - np.array([dim_offset, 0])
                else:
                    self.text_offset_x = 9
                    self.dim_line_anchor1 = self.dim_line_anchor1 + np.array([dim_offset, 0])
                    self.dim_line_anchor2 = self.dim_line_anchor2 + np.array([dim_offset, 0])
                

                self.text_offset_y = 0
                self.text_rotation = -90
            case _:
                raise Exception(f'{DimShape.__name__} cant handle {DataType.__name__} other then {DataType.XDim} oder {DataType.YDim}')

    def get_svg_string(self, class_str):
        dim_line_center = (self.dim_line_anchor1 + self.dim_line_anchor2)/2
        transform_x = dim_line_center[0] + self.text_offset_x
        transform_y = dim_line_center[1] + self.text_offset_y
        transform_rot = self.text_rotation

        svg_string = ''
        svg_string += f'<text class="{class_str}-text" transform="translate({transform_x} {transform_y}) rotate({transform_rot})">{self.dimension_text}</text>'

        if (self.dim_offset != 0):
            line1_x1, line1_y1 = self.pt1_transformed
            line1_x2, line1_y2 = self.dim_line_anchor1
            line2_x1, line2_y1 = self.pt2_transformed
            line2_x2, line2_y2 = self.dim_line_anchor2
            line3_x1, line3_y1 = self.dim_line_anchor1
            line3_x2, line3_y2 = self.dim_line_anchor2

            svg_string += f'\n<line class="{class_str}-line" x1="{line1_x1}" y1="{line1_y1}" x2="{line1_x2}" y2="{line1_y2}" />'
            svg_string += f'\n<line class="{class_str}-line" x1="{line2_x1}" y1="{line2_y1}" x2="{line2_x2}" y2="{line2_y2}" />'
            svg_string += f'\n<line class="{class_str}-line" x1="{line3_x1}" y1="{line3_y1}" x2="{line3_x2}" y2="{line3_y2}" />'

        return svg_string

    def get_boundry(self):
        return super().get_boundry()

class PathShape(Shape):
    def __init__(self, scale_divisor, points, reference):
        super().__init__(scale_divisor)

        referenced_points = list(map(lambda n: np.add(n,reference), points))
        mirrored_points = list(map(lambda n: self.invert_y(n), referenced_points))
        self.scaled_points = list(map(lambda n: self.cm_to_dots(n)/self.scale_divisor, mirrored_points))

    def get_svg_string(self, class_str):
        svg_string = f'<path class="{class_str}" d="'
        for i in range(0,len(self.scaled_points)):
            if (i == 0):
                svg_string += 'M'
            else:
                svg_string += 'L'

            svg_string += f'{self.scaled_points[i][0]} '
            svg_string += f'{self.scaled_points[i][1]} '

        svg_string += 'Z" />'

        return svg_string

    def get_boundry(self):
        xs = list(map(lambda n: n[0], self.scaled_points))
        ys = list(map(lambda n: n[1], self.scaled_points))

        return min(xs), max(xs), min(ys), max(ys)
    
class StepsShape(Shape):
    def __init__(self, scale_divisor, points, reference):
        super().__init__(scale_divisor)
        self.points_transformed = list(map(lambda n: self.transform_point(n, reference, scale_divisor), points))

    def transform_point(self, point:np.ndarray, reference:np.ndarray, scale_divisor):
        point_transformed = np.add(point,reference)
        point_transformed = self.invert_y(point_transformed)
        point_transformed = self.cm_to_dots(point_transformed)/scale_divisor
        return point_transformed

    def get_svg_string(self, class_str):
        step_centroids = list()
        svg_string = ''
        for i in range(0, int(len(self.points_transformed)/2)):
            if i > 0:
                svg_string += '\n'

            step_point1 = self.points_transformed[i]
            step_point2 = self.points_transformed[len(self.points_transformed)-i-1]

            step_centroids.append((step_point1+step_point2)/2)

            svg_string += SVGHelper.gen_line_string(step_point1, step_point2, class_str)

        svg_string += SVGHelper.gen_path_string(step_centroids, False, class_str)

        return svg_string 

    def get_boundry(self):
        return super().get_boundry()


class OpeningArgShape(Shape):
    def __init__(self, scale_divisor, points, reference):
        super().__init__(scale_divisor)

        referenced_points = list(map(lambda n: np.add(n,reference), points))
        mirrored_points = list(map(lambda n: self.invert_y(n), referenced_points))
        self.scaled_points = list(map(lambda n: self.cm_to_dots(n)/self.scale_divisor, mirrored_points))

    def get_svg_string(self, class_str):
        radius = np.linalg.norm(self.scaled_points[1]-self.scaled_points[0])

        v1 = self.scaled_points[1]-self.scaled_points[0]
        v2 = self.scaled_points[2]-self.scaled_points[0]
        angle = math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0])
        if (angle < 0): angle += 2*math.pi
        if (angle < math.pi):
            arc_dir = 1
        else:
            arc_dir = 0

        svg_string = f'<path class="{class_str}" d="'
        svg_string += f'M{self.scaled_points[0][0]} {self.scaled_points[0][1]} '
        svg_string += f'L{self.scaled_points[1][0]} {self.scaled_points[1][1]} '
        svg_string += f'A{radius} {radius} 0 0 {arc_dir} {self.scaled_points[2][0]} {self.scaled_points[2][1]} '
        svg_string += 'Z" />'

        return svg_string

    def get_boundry(self):
        return super().get_boundry()    
