#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from pane import *
from firebase import firebase
import time, cProfile, sys, json

def getFireBase():
	try:
            database = firebase.FirebaseApplication('https://arn-t-f8898.firebaseio.com/', None)
            data = database.get('/screen/simpleText', None)
            return data
	except:
	    print("Error:" + sys.exc_info()[0])
	    print("SimpleText refused by the server..")
            print("Let me sleep for 2 minutes")
            print("ZZzzzz...")
            time.sleep(120)
            print("Was a nice sleep, now let me continue...")
            pass

def main():
    data_str = json.dumps(getFireBase())
    data = json.loads(data_str)
    pane = Pane()
    box = Text_box(text = data['text'] ,alignment=data['alignment'], roll = 1, size=(62,1), position = (int(data['x']),int(data['y'])))
    pane.add_pane(box)
    pane.draw()
    pane.render()


if __name__ == '__main__':
    main()
