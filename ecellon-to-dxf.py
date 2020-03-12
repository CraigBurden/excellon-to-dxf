#!/usr/bin/env python

import argparse
import ezdxf
import code
import re

parser = argparse.ArgumentParser(description='Excellon to DXF Converter')
parser.add_argument("--input", required = True, help = "Input DRL file")
parser.add_argument("--output", default = "output.dxf", help = "Output DXF file")
parser.add_argument("--adjust", default = 0, help = "Adjustment to the Diameter of each drill")
args = parser.parse_args()

input_filename = args.input
output_filename = args.output
size_adjustment = float(args.adjust)

file = open(input_filename, 'r')
file_contents = file.read()

tool_details_text = re.findall(r"T(\d+)C(\d+\.?\d+)", file_contents)
tool_list = [{} for i in range(len(tool_details_text) + 1)]
for tool_index in range(len(tool_details_text)):
    tool_list[int(tool_details_text[tool_index][0])]['tool'] = int(tool_details_text[tool_index][0])
    tool_list[int(tool_details_text[tool_index][0])]['size'] = float(tool_details_text[tool_index][1])


drills_for_each_tool_text = re.findall(r"T(\d+)\s([XY\d\.\s-]+)", file_contents)
drills_list = []
for match_number in range(len(drills_for_each_tool_text)):
    temp = re.findall(r"X(-?\d+\.?\d+)Y(-?\d+\.?\d+)", drills_for_each_tool_text[match_number][1])
    for drill_index in range(len(temp)):
        drills_list.append({'tool':int(drills_for_each_tool_text[match_number][0]), 'x':float(temp[drill_index][0]), 'y':float(temp[drill_index][1])})

drawing = ezdxf.new('R2010')
modelspace = drawing.modelspace()

for drill in drills_list:
    modelspace.add_circle((drill['x'], drill['y']), ((tool_list[drill['tool']]['size'] + size_adjustment)/2))

drawing.saveas(output_filename)
file.close()
