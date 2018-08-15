#!/usr/bin/env/python
# -*- coding: utf-8 -*-
"""
py_output.py
Low level output functions 
A lot of this might have to be ported to C
"""

## IMPORTS
import spidev
import atexit
import time
import Queue, multiprocessing
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
from time import sleep
import ctypes

## CONSTANTS 
STROBE_PIN = 17 # Sets the pin to use for strobe output, 0 in board numbering equals 17 in BCM numbering
DEBUG = 0
MAX_SPEED = int(3E6) # Frequency of the SPI bus
# MAX_SPEED = int(4E5) # Frequency of the SPI bus
# NOTE: Setting this too low (under 5E5) will result in time outs for large buffers!
               
ADDRESS_MAP = [0b10101011,  # rätt
               0b10011011,  # rätt
               0b10111011,  # rätt
               0b10000111,  # rätt
               0b10100111,  # rätt
               0b10010111,  # rätt
               0b10110111,  # rätt
               0b10001111,  # rätt
               0b10101111,  # rätt
               0b10111111]  # ? Inte ikopplad
                     
## IO SETUP
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      # Initialize GPIO to use BOARD numbering for pins
GPIO.setup(STROBE_PIN, GPIO.OUT, initial=GPIO.LOW)
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 0 # sets SPI CPHA (0 = pulse clock high in middle of data)
spi.max_speed_hz = MAX_SPEED 

# C_TYPES
Lcd_bitmap = ctypes.c_byte*128
Segment_bitmap = ctypes.c_byte*40
c_funcs = ctypes.CDLL('./output_map.so')

def write_board(data):
    print 'apa'
    print "Type data", type(data)
    while isinstance(data, multiprocessing.queues.Queue):
        try: data = data.get(timeout = 0.1)
        except Queue.Empty: print 'adolf'
    print ('weee')
    for row in range(len(data)):
        write_row(row, data[row])
    latch()

def enable_address(row, immediate = False):
    """
    Prepare row for writing
    """
    if DEBUG > 0: print "writing to row", row
    row = ADDRESS_MAP[row]
    if DEBUG > 0: 
        print "Addres hex: {0} bin: {1}".format(hex(row), bin(row).rjust(10))
    if immediate: row &= 0x7F # immediate write mask
    write_byte(row)
    strobe()

def latch():
    """Update the board"""
    write_byte(0x01)
    strobe()

def strobe():
    """
    Pulse the strobe pin
    Makes the address cards evaluate their current content
    and will make the entire board latch (update) if 
    the first bit is 0
    """
    GPIO.output(STROBE_PIN, GPIO.HIGH)
    # sleep(0.0001)
    GPIO.output(STROBE_PIN, GPIO.LOW)


def write_byte(byte):
    """
    Write a single byte to the board
    used for addressing and latching
    """
    spi.xfer2([byte])

def write_row(row, data):
    """Output a list of segments to row  """
    enable_address(row) # Open row for writing
    if isinstance(data[0], (list, Segment_bitmap)):
        for d in data:
            spi.xfer2(list(d))
    else: 
        if MAX_SPEED < 1E6:
            for i in range(8):
                spi.xfer2(data[i*155:(i+1)*155])
        else: spi.xfer2(data)

def bmp2segment(lcd1, lcd2, segment):
    """
    Convert a segments, equivalent to a pair of LCD-displays
    to a list of bits that can be sent to the board.
    """
    return c_funcs.bmp2segment(lcd1, lcd2, segment)
  
def __at_exit():
    """ Releases all GPIO pins when the interpreter exits """
    GPIO.cleanup()
    spi.close()

atexit.register(__at_exit)


# TESTS ######################################################################
def address_test():
    # for i in xrange(127, 256, 2):
    # for i in xrange(127, 191, 2):
    # for i in xrange(151, 191, 2):
    # for i in xrange(161, 191, 2):
    # for i in xrange(181, 191, 2):
    # for i in xrange(185, 191, 2):
    # for i in xrange(185, 189, 2):
    for i in xrange(187, 189, 2):
        print "writing to ", i, hex(i)
        # enable_address(i)
        # to_send = [0xFF]*4096
        # to_send = [random.randint(0,255) for i in xrange(4096)] 
        strobe()
        write_byte(i)
        strobe()
        to_send = [0xAA]*40
        # for i in xrange(8):
        spi.xfer2(to_send)
        # write_row(i, to_send)
    latch()
    
def fill_panel():
    for i in xrange(10):
        print "writing to ", i
        # enable_address(i)
        # to_send = [0xFF]*4096
        # to_send = [random.randint(0,255) for i in xrange(4096)]
        byte = [0xFF]
        # to_send = ([0xFF]+byte*8+[0xFF])*40
        # to_send = (byte*8)*31*16
        # to_send = (byte*38)
        to_send = ([0x00]*40)+ ([0xAA]*40) + ([0xFF]*38)
        # to_send = ([0x00]*16 + [0xFF]*16)*31
        print "len to_send: ", len(to_send)
        # spi.xfer2(to_send)
        write_row(i, to_send)
        # time.sleep(1)
    # latch()    
    
def send_test():
    # for i in xrange(5, 10):
    for i in xrange(8,9):
        print "writing to ", i
        # enable_address(i)
        # to_send = [0xFF]*4096
        # to_send = [random.randint(0,255) for i in xrange(4096)]
        byte = [0x00]
        # to_send = ([0xFF]+byte*8+[0xFF])*40
        # to_send = (byte*38) + (byte*40)*30 
        to_send = (byte*39) #+ (byte*40) 
        print "len to_send: ", len(to_send)
        # spi.xfer2(to_send)
        write_row(i, to_send)
        # time.sleep(1)
    # latch()
    
def flash():
    for t in xrange(50):
        if t % 2: byte = [0x00]
        else: byte = [0xFF]
        for i in xrange(10):
            to_send = (byte*38) + (byte*40)*30 
            write_row(i, to_send)
        latch()
    
def one_pixel():
    row = 8
    to_send = ([0xFF]*38) + ([0xFF]*40)*30 
    write_row(row, to_send)
    to_send = [0x02] + [0x04] + [0x08] +[0x10]
    write_row(row, to_send)
    latch()
    
def main():
    # import random
    # send_test()
    one_pixel()
    # flash()
    # fill_panel()
    # address_test()
    # latch()
    # for i in xrange(255):
    # write_byte(1)
    # strobe()
    
if __name__ == '__main__': main()



