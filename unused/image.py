# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw
import pane



def main():
    im = Image.open("test.bmp")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 48)
    draw.text((10, 25), "world", font=font, fill=(0,0,0))
    im2 = im.convert(mode="1")
    im2.save("test.bmp", "BMP")

if __name__ == '__main__': main()