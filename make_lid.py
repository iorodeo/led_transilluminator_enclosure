from __future__ import print_function
from py2scad import *
import subprocess

make_dxf = True

x = 160.0
y = 100.0
thickness = 3.0
radius = 5.0
standoff_diam = 0.25*INCH2MM
hole_offset = 0.5*standoff_diam
hole_diam = 0.116*INCH2MM 
part_name = 'lid.scad'
proj_name = 'lid_proj.scad'
proj_dxf_name = 'lid_proj.dxf'


hole_list = []
for i in (-1,1):
    for j in (-1,1):
        hole_x = i*(0.5*x - 0.5*standoff_diam - hole_offset)
        hole_y = j*(0.5*y - 0.5*standoff_diam - hole_offset)
        hole_list.append((hole_x, hole_y, hole_diam))
        
lid = plate_w_holes(x,y,thickness,holes=hole_list,radius=radius)
lid_proj = Projection(lid)

print('creating: {0}'.format(part_name))
prog = SCAD_Prog()
prog.fn = 50
prog.add(lid)
prog.write(part_name)

print('creating: {0}'.format(proj_name))
prog = SCAD_Prog()
prog.fn = 50
prog.add(lid_proj)
prog.write(proj_name)

if make_dxf:
    print('converting: {0} --> {1}'.format(proj_name,proj_dxf_name))
    cmd = ['openscad', '-x', proj_dxf_name, proj_name]
    subprocess.call(cmd)















