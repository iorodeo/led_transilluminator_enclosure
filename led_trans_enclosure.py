from __future__ import print_function
from py2scad import *
import numpy


class LED_Trans_Enclosure(Basic_Enclosure):

    def __init__(self,params):
        super(LED_Trans_Enclosure,self).__init__(params)

    def make(self):
        self.set_inner_dimensions()
        self.add_dc_plug_hole()
        self.add_vent_holes()
        super(LED_Trans_Enclosure,self).make()
        self.make_upper_top()
        self.make_lower_top()

    def get_projection(self,**kwargs):
        part_list = super(LED_Trans_Enclosure,self).get_projection(**kwargs)
        return part_list

    def get_assembly(self,**kwargs):
        kwargs['show_top'] = False
        part_list = super(LED_Trans_Enclosure,self).get_assembly(**kwargs)
        try:
            explode_x, explode_y, explode_z = kwargs['explode']
        except KeyError:
            explode_x, explode_y, explode_z = 0, 0, 0
        try:
            show_top_lower = kwargs['show_top_lower']
        except KeyError:
            show_top_lower = True 
        try:
            show_top_upper = kwargs['show_top_lower']
        except KeyError:
            show_top_upper = True 

        # Translate lower and upper top into position
        x,y,z = self.params['inner_dimensions']
        top_wall_thickness = self.params['top_wall_thickness']
        top_z_shift = 0.5*z + 0.5*top_wall_thickness + explode_z
        top_lower = Translate(self.top_lower, v=(0.0,0.0,top_z_shift))

        top_z_shift += top_wall_thickness + explode_z
        top_upper = Translate(self.top_upper, v=(0.0,0.0,top_z_shift))

        if show_top_lower:
            part_list.append(top_lower)
        if show_top_upper:
            part_list.append(top_upper)
        return part_list

    def make_upper_top(self):
        self.make_top('top_upper')

    def make_lower_top(self):
        self.make_top('top_lower')
        hole_dx = self.params['led_cutout_dx']
        hole_dy = self.params['led_cutout_dy']
        cutout_hole = { 
                'panel'    : 'top_lower',
                'type'     : 'square',
                'location' : (0,0),
                'size'     : (hole_dx, hole_dy),
                }
        self.add_holes([cutout_hole])

    def make_top(self, name):
        thickness = self.params['top_wall_thickness']
        lid_radius = self.params['lid_radius']
        top = rounded_box(self.top_x, self.top_y, thickness, lid_radius, round_z=False)
        setattr(self,name,top)
        hole_list = []
        for hole in self.tab_hole_list + self.standoff_hole_list:
            if hole['panel'] != 'top':
                continue
            else:
                new_hole = dict(hole)
                new_hole['panel'] = name 
                hole_list.append(new_hole)
        self.add_holes(hole_list)

    def set_inner_dimensions(self):
        x = self.params['pcb_mount_hole_dx'] 
        x += 2*self.params['standoff_offset']
        x += self.params['standoff_diameter']
        y = self.params['pcb_mount_hole_dy'] 
        y += 2*self.params['standoff_offset']
        y += self.params['standoff_diameter']
        z = self.params['inner_height']
        self.params['inner_dimensions'] = x,y,z

    def add_pcb_mount_holes(self):
        # Create holes for mounting pcb
        for i in (-1,1):
            for j in (-1,1):
                hole_x = i*0.5*self.params['pcb_mount_hole_dx']
                hole_y = j*0.5*self.params['pcb_mount_hole_dy']
                hole = {
                        'panel'    : 'bottom',
                        'type'     : 'round',
                        'location' : (hole_x,hole_y),
                        'size'     : self.params['pcb_mount_hole_diam'],
                        }
                self.params['hole_list'].append(hole)

    def add_dc_plug_hole(self):
        x,y,z = self.params['inner_dimensions']
        hole_x = self.params['dc_jack_offset']
        hole_y = -0.5*z  
        hole_y += self.params['pcb_standoff_height']
        hole_y += self.params['pcb_thickness']
        hole_y += self.params['dc_jack_height']
        dc_plug_hole = { 
                'panel'     : 'right',
                'type'      : 'round',
                'location'  : (hole_x,hole_y),
                'size'      : self.params['dc_plug_diam'],
                } 
        self.params['hole_list'].append(dc_plug_hole)
        
    def add_vent_holes(self): 
        vent_hole_diameter = self.params['vent_hole_diameter']
        vent_hole_array_dx = self.params['vent_hole_array_dx']     
        vent_hole_array_dy = self.params['vent_hole_array_dy']     
        vent_hole_num_x = self.params['vent_hole_num_x']         
        vent_hole_num_y = self.params['vent_hole_num_y']

        x_pos_max = 0.5*vent_hole_array_dx - 0.5*vent_hole_diameter
        x_pos_min = -x_pos_max
        x_pos_array = numpy.linspace(x_pos_min, x_pos_max, vent_hole_num_x)

        y_pos_max = 0.5*vent_hole_array_dy - 0.5*vent_hole_diameter
        y_pos_min = -y_pos_max
        y_pos_array = numpy.linspace(y_pos_min, y_pos_max, vent_hole_num_y)

        hole_list = []
        for x_pos in x_pos_array:
            for y_pos in y_pos_array:
                hole = {
                        'panel'    : 'bottom', 
                        'type'     : 'round',
                        'location' : (x_pos,y_pos),
                        'size'     : vent_hole_diameter,
                        }
                hole_list.append(hole)
        self.params['hole_list'].extend(hole_list)

       

