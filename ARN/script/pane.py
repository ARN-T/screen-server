#!/usr/bin/env/python
# -*- coding: utf-8 -*-

"""
pane.py 


"""

# IMPORTS
import py_output, surface, fonts
import ctypes
import copy
import time
import cProfile
from PIL import Image
import PIL.ImageOps
import os, sys, time

c_funcs = ctypes.CDLL('./output_map.so')
# CONSTANTS
DEBUG = 0


class Pane(surface.Surface):
    """
    Extends the surface class with functionality for simple layouts
    """
    def __init__(self, parent = None, size = None, position = [0,0], background=surface.LCD_display()):
        self.segments = []  # Segments 
        self.writable = []  # Keeps track on if a segments pixels can be manipulated directly
        self.parent = parent
        self.background = background
        self.convert_processeses = []
        # self.convert_process2 = None
        if size and size[0] > 0 and size[1] > 0: self.max_size = list(size)
        else: self.max_size = [surface.SEGMENTS_WIDTH, surface.SEGMENTS_HEIGHT]
        self.size = self.max_size
        self.position = position
        self.__children = []
        self.__adjust_size_and_position()
    
    def __reinit_segments(self):
        new_segments = []
        self.writable = []
        for row in range(self.size[1]):
            if row >= len(self.segments):
                new_segments.append( [self.background for j in range(self.size[0])] )
            else:
                width_diff = self.size[0] - len(self.segments[row])
                if width_diff >= 0: 
                    new_row = self.segments[row] \
                            + [self.background for j in range(width_diff)]
                else: new_row = self.segments[row][:width_diff]
                new_segments.append(new_row)
            self.writable.append([False]*self.size[0])
        self.segments = new_segments
    
    def set_size(self, size = (0,0)):
        self.max_size[0] = surface.SEGMENTS_WIDTH if size[0] < 1 else size[0]
        self.max_size[1] = surface.SEGMENTS_HEIGHT if size[1] < 1 else size[1]        
        self.__adjust_size__and__position()
    
    def set_position(self, position = (0,0)):
        col = position[0]
        row = position[1]
        col = 0 if col < 0 else col
        row = 0 if row < 0 else row
        self.position = (col, row)
        self.__adjust_size__and__position()
    
    def get_position(self):
        if self.parent: 
            parent_pos = self.parent.get_position()
            return (self.position[0] + parent_pos[0],
                    self.position[1] + parent_pos[1])
        else: return self.position
        
    def __adjust_size_and_position(self):
        parent_size =  self.parent.size if self.parent \
                       else (surface.SEGMENTS_WIDTH, surface.SEGMENTS_HEIGHT)
        # Make sure pos is inside parent
        if self.position[0] > parent_size[0]: self.position[0] = parent_size[0] - 1  
        if self.position[1] > parent_size[1]: self.position[1] = parent_size[1] - 1
        # Calculate maximum tolerated size compared to parent
        max_tolerated_width = parent_size[0] - self.position[0]
        max_tolerated_height = parent_size[1] - self.position[1]
        self.size[0] = (max_tolerated_width
                        if self.max_size[0] > max_tolerated_width else self.max_size[0])
        self.size[1] = (max_tolerated_height
                        if self.max_size[1] > max_tolerated_height else self.max_size[1])
        # Layout child panes
        for c in self.__children:
            c.__adjust_size_and_position()
        self.__reinit_segments()
    
    def set_parent(self, parent):
        self.parent = parent
        self.__adjust_size_and_position()
    
    def get_root(self):
        return self.parent.get_root() if self.parent else self
    
    def add_pane(self, pane):
        self.__children.append(pane)
        pane.set_parent(self)
        
    def get_pane(self, index):
        return self.__children[index]
        
    def render(self, invert = False, noise = False):
        if not self.parent: surface.Surface.render(self, invert, noise)
        else: self.parent.render(invert, noise)
        
    def draw(self):
        for c in self.__children:
            c.draw()
        if DEBUG and not self.parent:
            repr_str = ""
            for row in xrange(self.size[1]):
                row_str = ""
                for col in xrange(self.size[0]):
                    row_str += self.segments[row][col].__repr__()
                repr_str += row_str + '\n'
            print repr_str
    
    def run(self, timer = 0):
        try: 
            if timer <= 0:
                while True:
                    self.draw()
                    self.render()
            else:
                t = time.time()
                while time.time() < t + timer:
                    self.draw()
                    self.render()
        except KeyboardInterrupt:
            sys.exit()

class Leaf_pane(Pane):
    
    def draw(self):
        Pane.draw(self)
        if self.parent:
            root = self.get_root()
            cur_pos = self.get_position()
            for row in xrange(0, self.size[1]):
                for col in xrange(0, self.size[0]):
                    try: 
                        root.set_segment(cur_pos[1] + row, cur_pos[0] + col, self.segments[row][col])
                    except:
                        print "Index out of range: row {0} col {1}".format(row, col)
    
    def add_pane(self, pane):
        pass
            
class Text_box(Leaf_pane):
    """
    Used for displaying text on a Pane
    """
    default_font = fonts.Font()
    def __init__(self, 
                 parent = None, 
                 size = None, 
                 position = (0,0),
                 text = "", 
                 alignment = "left",
                 fill_char = " ",
                 font = None, 
                 roll = 0):
        Pane.__init__(self, parent, size, position)
        self.text = text
        self.font = font or Text_box.default_font
        if isinstance(self.font, str): self.font = fonts.Font(filename=self.font)
        self.alignment = alignment
        self.fill_char = fill_char
        self.roll = roll
        self.frame_count = 0
        
    def set_text(self, text):
        self.text = text
        
    def get_aligned_text(self):
        no_characters = self.size[1]*self.size[0]
        if self.alignment == "center":
            text = self.text.center(no_characters, self.fill_char)
        elif self.alignment == "right":
            text = self.text.rjust(no_characters, self.fill_char)
        else:
            text = self.text.ljust(no_characters, self.fill_char)
        return text
    
    def layout_text(self):
        text = self.get_aligned_text()
        roll_distance = int(-(self.frame_count*-self.roll%len(text)))
        for row in xrange(self.size[1]):
            text_row_index = row * self.size[0] + roll_distance
            for col in xrange(self.size[0]):
                text_col_index = text_row_index + col
                self.segments[row][col] = self.font.get_glyph(text[text_col_index])
        
    def draw(self):
        self.layout_text()  
        self.frame_count += 1
        Leaf_pane.draw(self)
    
class Image_box(Leaf_pane):
    def __init__(self, file, parent = None, size = None, position = (0,0), offset=(0,0), invert = False):
        Pane.__init__(self, parent, size, position)
        self.file = file
        self.offset = offset
        self.set_image(file, offset, invert)
    
    # TODO: Should probably keep proportions and crop
    def set_image(self, file, offset = (0,0), invert = False):
        im = Image.open(file)
        segment_width = 8 + offset[0]
        segment_height = 16 + offset[1]
        im_width = segment_width * self.size[0]
        im_height = segment_height * self.size[1]
        im = im.resize((im_width, im_height))
        im = im.convert(mode="1")
        if invert: print("WARNING: Invert not implemented")
        for row in range(self.size[1]):
            for col in range(self.size[0]):
                left = col*segment_width
                upper = row*segment_height
                right = left + 8
                lower = upper + 16
                region = im.crop((left, upper, right, lower))
                self.segments[row][col] = surface.LCD_display(pixels = region.getdata())
    
    def __adjust_size_and_position(self):
        Pane.__adjust_size_and_position(self)
        self.set_image(self.file, self.offset)
        
class Sequence(Pane):
    def __init__(self, parent = None, size = None, position = (0,0)):
        Pane.__init__(self, parent, size, position)
        self.display_times = []
        self.current_frame = 0
        self.frame_count = 0
        self.number_of_frames = 0
        
    def add_pane(self, pane, display_time = 1):
        Pane.add_pane(self, pane)
        self.number_of_frames += 1
        if display_time < 1: display_time = 1
        self.display_times.append(display_time)
        
    def draw(self):
        if self.number_of_frames > 0:
            self.frame_count += 1
            if (self.frame_count > self.display_times[self.current_frame]):
                self.current_frame = (self.current_frame + 1) % self.number_of_frames
                self.frame_count = 0
            Pane.get_pane(self, self.current_frame).draw()
                
