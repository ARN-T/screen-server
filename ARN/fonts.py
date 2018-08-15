#!/usr/bin/env/python
# -*- coding: utf-8 -*-

"""
font.py

"""

# IMPORTS
import freetype
import py_output, surface

# CONSTANTS
DEFAULT_FONT_FILE = "u_vga16.bdf"
DEFAULT_SIZE = 16

class Font(object):
    def __init__(self, filename=DEFAULT_FONT_FILE, size=DEFAULT_SIZE):
        self.face = freetype.Face(filename)
        self.face.set_pixel_sizes(0, size)
        self.size = size
        self.glyphs = {}
    
    def glyph_for_character(self, char):
        # Let FreeType load the glyph for the given character and
        # tell it to render a monochromatic bitmap representation.
        self.face.load_char(char, freetype.FT_LOAD_RENDER |
                                  freetype.FT_LOAD_TARGET_MONO)
        return Glyph.from_glyphslot(self.face.glyph, char)

    def get_glyph(self, char):
        # print "using dict" if char in self.glyphs else "rendering {0}".format(char)
        if char in self.glyphs:
            return self.glyphs[char]
        else:
            return self.glyphs.setdefault(char, self.render_character(char))
    
    def render_character(self, char):
        glyph = self.glyph_for_character(char)
        return glyph #.bitmap
        
class Glyph(surface.LCD_display):
    def __init__(self, pixels, char):
        surface.LCD_display.__init__(self, pixels)
        self.char = char
        # self.bitmap = py_output.Lcd_bitmap #Bitmap(width, height, pixels)
    
    def __repr__(self):
        return self.char
    
    @staticmethod
    def from_glyphslot(slot, char):
        """Construct and return a Glyph object from a FreeType GlyphSlot."""
        pixels = Glyph.unpack_mono_bitmap(slot.bitmap)
        # width, height = slot.bitmap.width, slot.bitmap.rows
        return Glyph(pixels, char)

    @staticmethod
    def unpack_mono_bitmap(bitmap):
        """
        Unpack a freetype FT_LOAD_TARGET_MONO glyph bitmap into a bytearray where
        each pixel is represented by a single byte.
        """   
            
        # Allocate a bytearray of sufficient size to hold the glyph bitmap.
        data = bytearray(bitmap.rows * bitmap.width) 
        # Iterate over every byte in the glyph bitmap. Note that we're not
        # iterating over every pixel in the resulting unpacked bitmap --
        # we're iterating over the packed bytes in the input bitmap.
        for y in range(bitmap.rows):
            for byte_index in range(bitmap.pitch):

                # Read the byte that contains the packed pixel data.
                byte_value = bitmap.buffer[y * bitmap.pitch + byte_index]

                # We've processed this many bits (=pixels) so far. This determines
                # where we'll read the next batch of pixels from.
                num_bits_done = byte_index * 8

                # Pre-compute where to write the pixels that we're going
                # to unpack from the current byte in the glyph bitmap.
                rowstart = y * bitmap.width + byte_index * 8

                # Iterate over every bit (=pixel) that's still a part of the
                # output bitmap. Sometimes we're only unpacking a fraction of a byte
                # because glyphs may not always fit on a byte boundary. So we make sure
                # to stop if we unpack past the current row of pixels.
                for bit_index in range(min(8, bitmap.width - num_bits_done)):
                    # Unpack the next pixel from the current glyph byte.
                    bit = byte_value & (1 << (7 - bit_index))
                    # Write the pixel to the output bytearray. We ensure that `off`
                    # pixels have a value of 0 and `on` pixels have a value of 1.
                    data[rowstart + bit_index] = 1 if bit else 0
        
        # Se till att bokstaven är centrerad och på linjen oavsett storlek
        h_diff = surface.LCD_HEIGHT - bitmap.rows
        w_diff = surface.LCD_WIDTH - bitmap.width
        
        lcd_bitmap = py_output.Lcd_bitmap()
        
        if h_diff >= 0: 
            lcd_start_row = h_diff
            bmp_start_row = 0
        else: 
            lcd_start_row = 0 
            bmp_start_row = abs(h_diff)
        if w_diff >= 0: 
            lcd_start_col = w_diff // 2
            bmp_start_col = 0
            lcd_end_col = w_diff // 2 + bitmap.width
            bmp_end_col = bitmap.width
        else: 
            lcd_start_col = 0 
            bmp_start_col = abs(w_diff)//2
            lcd_end_col = surface.LCD_WIDTH
            bmp_end_col = abs(w_diff)//2 + surface.LCD_WIDTH
        
        # print "BMP height: ", bitmap.rows, "width: ", bitmap.width, "start row: ", bmp_start_row
        
        for row in range(max(lcd_start_row, bmp_start_row), surface.LCD_HEIGHT):
            lcd_index = surface.LCD_WIDTH * row + lcd_start_col
            bmp_index = bitmap.width * (row - lcd_start_row) + bmp_start_col 
            for col in range(0, min(lcd_end_col, bmp_end_col)):
                try: val = data[bmp_index + col]
                except IndexError:
                    print "BMP index ", bmp_index + col
                    raise IndexError("Tried accesing index", bmp_index + col, "out of", len(data)-1)
                try: lcd_bitmap[lcd_index + col] = val
                except IndexError:
                    print "LCD index ", lcd_index + col
                    raise IndexError("Tried accesing index", lcd_index + col, "out of", len(lcd_bitmap)-1)
        return lcd_bitmap

        
class Bitmap(object):
    """
    A 2D bitmap image represented as a list of byte values. Each byte indicates
    the state of a single pixel in the bitmap. A value of 0 indicates that
    the pixel is `off` and any other value indicates that it is `on`.
    """
    def __init__(self, width, height, pixels=None):
        self.width = width
        self.height = height
        self.pixels = pixels or bytearray(width * height)

    def __repr__(self):
        """Return a string representation of the bitmap's pixels."""
        rows = ''
        for y in range(self.height):
            for x in range(self.width):
                rows += '*' if self.pixels[y * self.width + x] else ' '
            rows += '\n'
        return rows
        
def main():
    fnt = Font("u_vga16.bdf", 16)
    ch = fnt.get_glyph(u"T")
    repr(ch)
    print ch
      
if __name__ == '__main__': main() 