#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from pane import *
import time, cProfile, sys

def wupp():
    pane = Pane()
    pane2 = Pane()
    box = Text_box(text = u"Välkommen till Flygsektionen!", roll = 1, alignment = "center", size=(62,1))
    box2 = Text_box(text = u"ÖPH ser dig!", roll = 1, alignment = "center", size=(62,1))
    img = Image_box(file = "logo_small.png", position = (7, 1), size = (45,8), offset=(2,12))
    img2 = Image_box(file = "logo_small.png", position = (7, 1), size = (45,8), offset=(2,12))
    pane.add_pane(box)
    pane.add_pane(img)
    pane2.add_pane(img2)
    pane2.add_pane(box2)
    pane.draw()
    pane.render()
    pane2.draw()
    pane2.render()

def sequence_ex():
    pane = Pane()
    box = Text_box(text = u"Usted que olvidó a su perro en el frente debe", alignment = "center", size=(62,1),position = (7, 1))
    box2 = Text_box(text = u"estacionarlo inmediatamente en otro lugar", alignment = "center", size=(62,1),position = (8, 1))
    #img = Image_box(file = "logo_small.png", position = (7, 1), size = (45,8), offset=(2,12))
    #img2 = Image_box(file = "wupp.bmp", position = (7, 1), size = (45,8), offset=(2,10))
    seq = Sequence()
    pane.add_pane(box)
    pane.add_pane(box2)
    #seq.add_pane(img, 3000)
    #seq.add_pane(img2, 5)
    pane.add_pane(seq)
    pane.run()

def image():
    pane = Pane()
    img = Image_box(file = "logo_small.png", position = (7, 1), size = (45,8))
    pane.add_pane(img)
    pane.draw()
    pane.render()

def image_offset():
    pane = Pane()
    img = Image_box(file = "logo_small.png", position = (7, 1), size = (45,8), offset=(2,12))
    pane.add_pane(img)
    pane.draw()
    pane.render()

def text():
    """Displays text"""
    pane = Pane()
    text_left = Text_box(text = u"Hello left!",
                         size=(62,1),
                         position = (0, 1),
                         alignment = "left")
    text_center = Text_box(text = u"Hello center!",
                           size=(62,1),
                           position = (0, 2),
                           alignment = "center")
    text_right = Text_box(text = u"Hello right!",
                          size=(62,1),
                          position = (0, 4),
                          alignment = "right")
    pane.add_pane(text_left)
    pane.add_pane(text_center)
    pane.add_pane(text_right)
    pane.draw()
    pane.render()

def panes():
    pane = Pane()
    box = Text_box(text = u"Välkomna till Flygsektionen!",
                   alignment = "center",
                   position = (0, 8),
                   size=(62,1))
    img = Image_box(file = "logo_small.png",
                    position = (7, 0),
                    size = (45,8),
                    offset=(2,12))
    pane.add_pane(box)
    pane.add_pane(img)
    pane.draw()
    pane.render()

def funkis():
    pane = Pane()
    pane.fill_rect(color = 1)
    img = Image_box(file = "disney2.png",
                    position = (7, 0),
                    size = (45,8),
                    offset=(2,12))
    text = Text_box(text = "PICTURES",
                   alignment = "center",
                   position = (0, 8),
                   size=(62,1))
    pane.add_pane(img)
    pane.add_pane(text)
    pane.draw()
    pane.render(invert = True)

def main():
    # text()
    # image()
    # image_offset()
    # panes()
     wupp()
    #sequence_ex()
    # funkis()

if __name__ == '__main__': main()
