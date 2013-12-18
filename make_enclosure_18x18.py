"""
Creates an enclosure for the 18x18 blue LED PCB
"""
from __future__ import print_function
import os
import subprocess
from py2scad import *
from led_trans_enclosure import LED_Trans_Enclosure


INCH2MM = 25.4
PROJECTION = True
MAKE_DXF = True
model = '18x18'

params = {
        'inner_height'            : 1.2505*INCH2MM,
        'pcb_mount_hole_dx'       : 6.9291*INCH2MM,
        'pcb_mount_hole_dy'       : 5.3543*INCH2MM,
        'pcb_mount_hole_diam'     : 0.1160*INCH2MM,
        'wall_thickness'          : 3.0, 
        'top_upper_thickness'     : 1.5,
        'top_middle_thickness'    : 1.5,
        'top_lower_thickness'     : 3.0,
        'lid_radius'              : 0.25*INCH2MM,  
        'top_x_overhang'          : 0.10*INCH2MM,
        'top_y_overhang'          : 0.08*INCH2MM,
        'bottom_x_overhang'       : 0.25*INCH2MM,
        'bottom_y_overhang'       : 0.08*INCH2MM, 
        'lid2front_tabs'          : (0.2,0.5,0.8),
        'lid2side_tabs'           : (0.2,0.5,0.8),
        'side2side_tabs'          : (0.5,),
        'lid2front_tab_width'     : 0.5*INCH2MM,
        'lid2side_tab_width'      : 0.5*INCH2MM, 
        'side2side_tab_width'     : 0.5*INCH2MM,
        'tab_depth_top'           : 4.55,
        'tab_depth_bot'           : 3.0,
        'tab_depth_side'          : 3.0,
        'standoff_diameter'       : 0.25*INCH2MM,
        'standoff_offset'         : 0.10*INCH2MM, 
        'standoff_hole_diameter'  : 0.116*INCH2MM,   
        'pcb_standoff_height'     : (3.0/16.0)*INCH2MM,
        'pcb_thickness'           : 0.061*INCH2MM,
        'dc_jack_height'          : 0.25*INCH2MM,
        'dc_jack_offset_x'        : 1.8898*INCH2MM,
        'switch_height'           : 7.2, 
        'switch_offset_x'         : 0.7087*INCH2MM, 
        'switch_hole_x'           : 0.40*INCH2MM,
        'switch_hole_y'           : 6.0,
        'switch_hole_radius'      : 1.0,
        'dc_plug_diam'            : 0.38*INCH2MM,
        'led_cutout_dx'           : 140,
        'led_cutout_dy'           : 140,
        'vent_hole_diameter'      : 0.15*INCH2MM,
        'vent_hole_array_dx'      : 2.718*INCH2MM,
        'vent_hole_array_dy'      : 2.41*INCH2MM,
        'vent_hole_num_x'         : 6,
        'vent_hole_num_y'         : 5,
        'hole_list'               : [],

        }

proj_file_list = []

enclosure = LED_Trans_Enclosure(params)
enclosure.make()

part_assembly = enclosure.get_assembly(
        explode=(0,0,10),
        show_top_upper = False, 
        show_top_middle = True,
        show_bottom = True,
        show_left =  True,
        show_right = True,
        show_front = True,
        show_back = True,
        show_standoffs = False,
        )
part_projection = enclosure.get_projection(
        project=PROJECTION,
        exclude_list=['top']
        )

prog_assembly = SCAD_Prog()
prog_assembly.fn = 50
prog_assembly.add(part_assembly)
prog_assembly.write('enclosure_assembly_{0}.scad'.format(model))

prog_projection = SCAD_Prog()
prog_projection.fn = 50
prog_projection.add(part_projection)
filename = 'enclosure_projection_{0}.scad'.format(model)
prog_projection.write(filename)
proj_file_list.append(filename)

top_name_list = ['top_middle', 'top_lower', 'top_upper']
for top_name in top_name_list:
    prog_top_proj = SCAD_Prog()
    prog_top_proj.fn = 50
    top = getattr(enclosure,top_name)
    if PROJECTION:
        top_proj = Projection(top)
    else:
        top_proj = top
    prog_top_proj.add(top_proj)
    filename = '{0}_projection_{1}.scad'.format(top_name,model)
    prog_top_proj.write(filename)
    proj_file_list.append(filename)

if MAKE_DXF:
    for scad_name in proj_file_list:
        base_name, ext = os.path.splitext(scad_name)
        dxf_name = '{0}.dxf'.format(base_name)
        cmd = ['openscad', '-x', dxf_name, scad_name]
        print('{0} --> {1}'.format(scad_name, dxf_name))
        print(' '.join(cmd))
        subprocess.call(cmd)




