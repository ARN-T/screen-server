#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from pane import *
from firebase import firebase
import time, cProfile, sys

def main():
    #text = getFireBase()
    pane = Pane()
    box = Text_box(text = u"Daily quote...",alignment="center", position = (0,2), size=(62,1))
    box2 = Text_box(text = u"aölskdjfasökldjf.",alignment="center", position = (0,5), size=(62,1))
    box3 = Text_box(text = u"- Robert H. Schiuller",alignment="center", position = (0,6), size=(62,1))
    pane.add_pane(box)
    pane.add_pane(box2)
    pane.add_pane(box3)
    pane.draw()
    pane.render()

def getFireBase():
	database = firebase.FirebaseApplication('https://arn-t-f8898.firebaseio.com/', None)
	text = database.get('/screen/simpleText', None)
	return text

if __name__ == '__main__':
    main()
