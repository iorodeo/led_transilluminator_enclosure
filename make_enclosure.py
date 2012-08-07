"""
Creates and enclosure for the LED based transilluminator.
"""
from __future__ import print_function
import os
import subprocess
from py2scad import *
from led_trans_enclosure import LED_Trans_Enclosure


INCH2MM = 25.4
PROJECTION = True 
MAKE_DXF = True 

params = {
        'inner_height'            : 1.208*INCH2MM,
        'pcb_mount_hole_dx'       : 4.1953*INCH2MM,
        'pcb_mount_hole_dy'       : 2.1894*INCH2MM,
        'pcb_mount_hole_diam'     : 0.1160*INCH2MM,
        'wall_thickness'          : 3.0, 
        'top_wall_thickness'      : 1.5,
        'lid_radius'              : 0.25*INCH2MM,  
        'top_x_overhang'          : 0.10*INCH2MM,
        'top_y_overhang'          : 0.08*INCH2MM,
        'bottom_x_overhang'       : 0.25*INCH2MM,
        'bottom_y_overhang'       : 0.08*INCH2MM, 
        'lid2front_tabs'          : (0.2,0.5,0.8),
        'lid2side_tabs'           : (0.25, 0.75),
        'side2side_tabs'          : (0.5,),
        'lid2front_tab_width'     : 0.5*INCH2MM,
        'lid2side_tab_width'      : 0.5*INCH2MM, 
        'side2side_tab_width'     : 0.5*INCH2MM,
        'standoff_diameter'       : 0.25*INCH2MM,
        'standoff_offset'         : 0.05*INCH2MM, 
        'standoff_hole_diameter'  : 0.116*INCH2MM,   
        'pcb_standoff_height'     : (5.0/16.0)*INCH2MM,
        'pcb_thickness'           : 0.061*INCH2MM,
        'dc_jack_height'          : 0.25*INCH2MM,
        'dc_jack_offset'          : -0.415*INCH2MM,
        'dc_plug_diam'            : 0.38*INCH2MM,
        'led_cutout_dx'           : 2.718*INCH2MM,
        'led_cutout_dy'           : 2.41*INCH2MM,
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
        show_top_upper = True, 
        show_top_lower = True,
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
prog_assembly.write('enclosure_assembly.scad')

prog_projection = SCAD_Prog()
prog_projection.fn = 50
prog_projection.add(part_projection)
filename = 'enclosure_projection.scad'
prog_projection.write(filename)
proj_file_list.append(filename)

top_name_list = ['top_lower', 'top_upper']
for top_name in top_name_list:
    prog_top_proj = SCAD_Prog()
    prog_top_proj.fn = 50
    top = getattr(enclosure,top_name)
    if PROJECTION:
        top_proj = Projection(top)
    else:
        top_proj = top
    prog_top_proj.add(top_proj)
    filename = '{0}_projection.scad'.format(top_name)
    prog_top_proj.write(filename)
    proj_file_list.append(filename)

if MAKE_DXF:
    for scad_name in proj_file_list:
        base_name, ext = os.path.splitext(scad_name)
        dxf_name = '{0}.dxf'.format(base_name)
        cmd = ['openscad', '-o', dxf_name, scad_name]
        print('{0} --> {1}'.format(scad_name, dxf_name))
        print(' '.join(cmd))
        subprocess.call(cmd)




