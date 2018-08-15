#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""
surface.py 

"""

# IMPORTS
import py_output
import ctypes
import copy
import time
import Queue, atexit, multiprocessing
import cProfile

# CONSTANTS
PIXELS_HEIGHT = 16*10
PIXELS_WIDTH = 8*62
SEGMENTS_HEIGHT = 10
SEGMENTS_WIDTH = 62
LCD_HEIGHT = 16
LCD_WIDTH = 8

# CONFIG
DRAW_BUFFER = 4
DEBUG = 1

c_funcs = ctypes.CDLL('./output_map.so')

class Render_process(multiprocessing.Process):
    
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
            try:
                to_draw = self.queue.get()
                if not to_draw: 
                    return  # Shutdown process if empty data is sent
                for row in range(len(to_draw)):
                    py_output.write_row(row, to_draw[row])
                py_output.latch()
            except KeyboardInterrupt:
                print "Keyboard interrupt in render queue"

render_queue = multiprocessing.Queue(DRAW_BUFFER)
render_process = Render_process(render_queue)
render_process.start()
            
class Convert_process(multiprocessing.Process):
    
    def __init__(self, segments, noise = False, invert = False):
        multiprocessing.Process.__init__(self)
        self.segments = segments
        self.noise = noise
        self.invert = invert
    
    def run(self):
        to_send = []
        for row in self.segments: 
            to_send.append(convert_segments(row, self.noise, self.invert))
        if DEBUG > 1: print "Sending to queue"
        render_queue.put(to_send)
        if DEBUG > 1: print "Done sending"

def convert_segments(row, noise = False, invert = False):
    sendable = [] 
    for lcd_index in xrange(0, len(row), 2):
        segment = py_output.Segment_bitmap()
        c_funcs.bmp2segment(row[lcd_index].pixels, row[lcd_index+1].pixels, segment)
        if not noise: c_funcs.fix_segment(segment)
        if not invert: c_funcs.invert_segment(segment)
        sendable = list(segment) + sendable
    return sendable
            
class Surface(object):
    
    # render_queue = multiprocessing.Queue(DRAW_BUFFER)
    # render_process = Render_process(render_queue)
    # render_process.start()
    convert_processeses = []
    
    def __init__(self):
        self.segments = []  # Segments 
        self.writable = []  # Keeps track on if a segments pixels can be manipulated directly
        self.width = SEGMENTS_WIDTH
        self.height = SEGMENTS_HEIGHT
        # self.convert_processes = []
        # self.convert_process2 = None
        for i in range(self.height):
            self.segments.append( [LCD_display() for j in range(self.width)] )
            self.writable.append([True]*self.width)
        
    def put_pixel(self, row, col, color):
        segment_row = row // SEGMENTS_HEIGHT
        segment_col = col // SEGMENTS_WIDTH
        if not self.writable[segment_row][segment_col]:
            new_display = LCD_display(self.get_segment(segment_row, segment_col))
            self.set_segment(segment_row, segment_col, new_display)
            self.writable[segment_row][segment_col] = True
        pixel_row = row % SEGMENTS_HEIGHT
        pixel_col = col % SEGMENTS_WIDTH
        segment = self.get_segment(segment_row, segment_col)
        segment[pixel_row*8 + pixel_col] = color
    
    def multi_render(self):
        pass
        # pool = multiprocessing.Pool(4)
        # return pool.map(convert_segments, self.segments)
    
    def render(self, invert = False, noise = False):
        
        processes = Surface.convert_processeses
        # Check if there are already enough processes runing
        while len(processes) > DRAW_BUFFER-2:
            processes = [p for p in Surface.convert_processeses if p.is_alive()]
        # Create and append the new process
        processes.append(Convert_process(self.segments, noise, invert))
        processes[-1].start()
        # Remove and join any finished processes
        dead_processes = [p for p in Surface.convert_processeses if not p.is_alive()]
        for dp in dead_processes: dp.join()
        Surface.convert_processeses = processes
        # rows = []
        # for row_index in xrange(SEGMENTS_HEIGHT):
            # if DEBUG > 0: print "rendering row ", row_index 
            # row = self.segments[row_index]
            # sendable = [] 
            # for lcd_index in xrange(0, len(row), 2):
                # segment = py_output.Segment_bitmap()
                # c_funcs.bmp2segment(row[lcd_index].pixels, row[lcd_index+1].pixels, segment)
                # if not noise: c_funcs.fix_segment(segment)
                # if not invert: c_funcs.invert_segment(segment)
                # sendable = list(segment) + sendable            
            # rows.append(sendable)
        # render_queue.put(rows)
    
    def send(to_draw):
        for row in range(len(to_draw)):
                py_output.write_row(row, to_draw[row])
        py_output.latch()
    
    def clear(self):
        self.fill_rect()
   
    def fill_rect(self, color=0, 
                  display_model = None, 
                  rows = (0,SEGMENTS_HEIGHT), 
                  columns = (0,SEGMENTS_WIDTH), 
                  fast = True):
        """
        Fills a rectangle on the board with a color or copies of a display
        """
        if not display_model: display_model = LCD_display(color = color)
        for row in range(*rows):
            for col in range(*columns):
                if fast: 
                    self.segments[row][col] = display_model
                    self.writable[row][col] = False
                else: 
                    self.segments[row][col] = LCD_display(display_model)
                    self.writable[row][col] = True
    
    def get_segment(self, row, col):
        return  self.segments[row][col]
    
    def set_segment(self, row, col, segment):
        self.segments[row][col] = segment
        # try: self.segments[row][col] = segment
        # except IndexError:
            # raise IndexError("list index out of range at row {0} col {1} out of ".format(row, col))
    
    def get_size(self):
        return (self.width, self.height)
    
    def __getitem__(self, tup):
        row, col = tup
        segment = self.get_segment(row // SEGMENTS_HEIGHT, col // SEGMENTS_WIDTH)
        return segment[row % SEGMENTS_HEIGHT][col % SEGMENTS_WIDTH]
        
    def __setitem__(self, tup, color):
        row, col = tup
        self.put_pixel(row, col, color)
    
    def __repr__(self):
        base = ""
        
    
class LCD_display(object):
    """ Represents one LCD display"""
    HEIGHT = 16
    WIDTH = 8
    def __init__(self, pixels = None, color = 0):
        self.pixels = py_output.Lcd_bitmap()
        self.width, self.height = LCD_display.WIDTH, LCD_display.HEIGHT 
        if pixels:
            for i in range(len(self.pixels)):
                self.pixels[i] = 1 if pixels[i] else 0
                    
        elif color:
            #[True]*LCD_display.HEIGHT*LCD_display.WIDTH
            for i in range(len(self.pixels)):
                self.pixels[i] = 1
    
    def __getitem__(self, pos):
        return self.pixels[pos]
    
    def __getstate__(self):
        return {'pixels':list(self.pixels), 
                'width':self.width,
                'height':self.height}
                
    def __setstate__(self, state):
        self.pixels = py_output.Lcd_bitmap(*state['pixels'])
        self.width = state['width']
        self.height = state['height']
    
    def __setitem__(self, pos, color):
        self.pixels[pos]
    
    def __repr__(self):
        return 'X'
        rows = ''
        for y in range(LCD_display.HEIGHT):
            for x in range(LCD_display.WIDTH):
                rows += '*' if self.pixels[y * LCD_display.WIDTH + x] else ' '
            rows += '\n'
        return rows

def __at_exit():
    """ Releases all GPIO pins when the interpreter exits """
    # Surface.render_thread.running = False
    # Surface.render_thread.join()
    # Surface.render_process.running = False
    # Surface.render_queue.put(None)
    for p in Surface.convert_processeses:
        p.join()
    render_queue.put(None)
    render_process.join()

atexit.register(__at_exit)
        
def main():
    # c_funcs = ctypes.CDLL('./output_map.so')
    # lcd1 = LCD_display()
    # lcd2 = LCD_display()
    # c_funcs.bmp2segment(lcd1.pixels, lcd2.pixels)
    py_output.c_funcs.myprint()
    surface = Surface()
    surface.fill_rect(color = 1)
    surface.render()
    # apa = LCD_display()
    # adolf = apa
    # groen = LCD_display(apa)
    # apa[0][0] = True
    # adolf[0][15] = True
    # adolf = LCD_display(color = 1)
    # print apa
    # print groen
    # print adolf
    
if __name__ == '__main__': cProfile.run("main()")

    
    
    
    
    
    
    
    
    
    
