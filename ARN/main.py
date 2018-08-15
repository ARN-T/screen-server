#!/usr/bin/env/python
# -*- coding: utf-8 -*-

from pane import *
import time, cProfile, sys, os

# Firebase
from firebase import firebase


database = firebase.FirebaseApplication('https://arn-t-f8898.firebaseio.com/', None)
database.put('screen/namer','index',0)

def namer():
    try:
    	text = database.get('/screen/namer', None)
    	return text
    except:
	print(time.ctime())
	print("Error:" + sys.exc_info()[0])
	print("Script namer refused by the server..")
        print("Let me sleep for 2 minutes")
        print("ZZzzzz...")
        time.sleep(120)
        print("Was a nice sleep, now let me continue...")
        pass

def main():
    while True:
	try:
	    nameObj = namer()
	    n = nameObj['index']
	except:
	    n = 0

	if n == 0:
	    try:
		print(time.ctime())
            	print("Running: " + nameObj['name'])
	    	database.put('screen/namer','index',1)
		print(" ")
	    except:
		print('Post-fail to Firebase.')
		print('Trying again..')    
		pass
	else: pass
        os.system('python ' + nameObj['name'])
        time.sleep(5)


if __name__ == '__main__':main()
