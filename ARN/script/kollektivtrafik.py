#!/usr/bin/env/python
#-*- coding:utf-8 -*-
from pane import *
import requests, json, time, cProfile, sys
from time import strftime, localtime
from firebase import firebase

def displayTimes(station, farkoster, storningsinfo, dt):
	bs = []
	mt = []
	ts = []
	tm = []
	sh = []
	res = [bs, mt, ts, tm, sh, []]

	#API:er tenderar att använda formatet json. Läs mer här om API:er i python: https://www.dataquest.io/blog/python-api-tutorial/
	Format = 'json'

	#SL platsuppslag, läs mer om API:et här: https://www.trafiklab.se/api/sl-platsuppslag/dokumentation
	KeyPlatsUpp = '7f2a0c4e87b143f4beaca5dc203dd031'
	SearchString = station
	StationsOnly = True
	MaxResults = 1

	r1 = requests.get('http://api.sl.se/api2/typeahead.' + Format + '?key=' + KeyPlatsUpp + '&searchstring=' + SearchString + '&stationsonly=' + str(StationsOnly) + '&maxresults=' + str(MaxResults))
	c1 = json.loads(r1.content)
	SiteId = c1["ResponseData"][0]["SiteId"]
	stt = c1["ResponseData"][0]["Name"]
	res[5] = stt
	#print 'Departure times for '+ c1["ResponseData"][0]["Name"]


	#SL realtidsinformation, läs mer om API:et här: https://www.trafiklab.se/node/15754/documentation
	KeyRealTid = 'a321eb0ce9f146ca943e56d70fa4823b'
	TimeWindow = dt #max 60 min

	#Ange vilken kollektivtrafik man vill ska visas:
	Buses = farkoster[0]
	Metro = farkoster[1] #tunnelbana
	Trains = farkoster[2] #pendeltåg
	Trams = farkoster[3] #roslagsbana
	Ships = farkoster[4]

	r2 = requests.get('http://api.sl.se/api2/realtimedeparturesV4.' + Format + '?key=' + KeyRealTid + '&siteid=' + SiteId + '&timewindow=' + str(TimeWindow) + '&Bus=' + str(Buses) + '&Metro=' + str(Metro) + '&Train=' + str(Trains) + '&Tram=' + str(Trams) + '&Ship=' + str(Ships))
	c2 = json.loads(r2.content)
	rd = c2["ResponseData"]
	t = [rd["Buses"], rd["Metros"], rd["Trains"], rd["Trams"], rd["Ships"]]
	st = ["-- Bussar -- ", "-- Tunnelbana -- ", "-- Pendeltåg --", "-- Roslagsbana --", "-- Båtar --"]

 	for i in range(0, 5): #i motsv vilken farkost
 		tt = t[i]
 		if farkoster[i] == True and len(t[i]) != 0:
 			#print st[i]
 			for j in range(0, len(t[i])): #j motsv vilken vi tittar på
 				if i == 0:
 					#print tt[j]["LineNumber"] + ' ' + tt[j]["Destination"] + ': ' + tt[j]["DisplayTime"] #Special för bussar
 					res[0].append(tt[j]["LineNumber"] + ' ' + tt[j]["Destination"] + ': ' + tt[j]["DisplayTime"])
 				else:
 					#print tt[j]["Destination"] + ': ' + tt[j]["DisplayTime"]
 					res[i].append(tt[j]["Destination"] + ': ' + tt[j]["DisplayTime"])
 			#print "\n"

	#SL störningsinformation, läs mer om API:et här: https://www.trafiklab.se/node/12605/documentation
	if storningsinfo == True:
		KeyTrafikLege = 'ba951888f9d24f579e157b627b53a061'
		r3 = requests.get('http://api.sl.se/api2/trafficsituation.' + Format + '?key=' + KeyTrafikLege)
		c3 = json.loads(r3.content)
		rd3 = c3["ResponseData"]["TrafficTypes"]
		#print '--Störningsinformation--'
		for i in rd3:
			if i["HasPlannedEvent"] == True:
				print i["Name"]
				for j in i["Events"]:
					print j["Message"]
				print "\n"

	return res

#function that prints on ARN board and does not make any calls to an API
def printOnScreen(buses, metro, trains, trams, ships, sttn, time, firebaseText):
	pane = Pane()

	d = 3
	tBox = Text_box(text =  u"hej", position = (1, 1), size = (62, 1), alignment = "left")
	tBox2 = Text_box(text =  u"Det tar ca 5 min att gå...", position = (1, 8), size = (31, 1), alignment = "left")
	pane.add_pane(tBox)
	pane.add_pane(tBox2)

	#metro:
	mtBoxL = []
	if len(metro) > 10-d: #10 är max antal rader på tavlan
		k = 10-d
	else:
		k = len(metro)
	for i in range(0, k):
		mtBoxL.append(Text_box(text = metro[i], position = (1, i+d), size = (62, 1), alignment = "left"))
		pane.add_pane(mtBoxL[i])

	#buses:
	bsBoxL = []
	if len(buses) > 10-1:
		k2 = 10-1
	else:
		k2 = len(buses)
	for i in range(0, k2):
		bsBoxL.append(Text_box(text = buses[i], position = (29, i+1), size = (33, 1), alignment = "right"))
		pane.add_pane(bsBoxL[i])

	#Add data from firebase
	textfield = Text_box(text = u"Lokaltrafik", roll = 1, size=(62,1), position = (0,0), alignment = "right")
	pane.add_pane(textfield)

	pane.draw()
	pane.render()

def getFireBase():
	database = firebase.FirebaseApplication('https://arn-t-f8898.firebaseio.com/', None)
	text = database.get('/screen', None)
	return text

def sortMetro(mData, minTime):
	#sorterar metro data så att tidigare tåg kommer först
	d = {} #dictionary for storing original values
	t = []


	for i in range(0, len(mData)):

		if ":" in mData[i][len(mData[i].strip())-3:]:
			galenskap = mData[i][len(mData[i].strip())-5:]
			cTime = strftime("%H:%M", localtime()) #current time
			ch = int(cTime[:2]) #current hours
			cm = int(cTime[3:]) #current minutes
			h = int(galenskap[:2])
			m = int(galenskap[3:])
			dm = (60*h + m) - (60*ch + cm) #the amount of minutes to coming departure
			namn = mData[i][:len(mData[i].strip())-7]
			mData[i] = namn + ": " + str(dm) + " min"




	for i in range(0, len(mData)):
		tempTS = mData[i].split(': ')
		tempTS = tempTS[1].strip() #take second element

		if tempTS == 'Nu': #add 0 so that Nu comes first
			tempTS = 0*10 + i
		else:
			tempTS = tempTS.split(' min')
			tempTS = int(tempTS[0])
			if tempTS > 5:
				tempTS = tempTS*10 + i #sätt en indexidentifier i slutet
				t.append(tempTS)
				d[i] = mData[i]

	t.sort()
	res = []
	for i in range(0, len(t)):
		tt = t[i] #temporary storage of minutes and marker
		idm = tt%10 #identifying marker
		try:
			res.append(d[idm]) #add from dictionary
		except:
			None

	return res

def filterBuses(bData, minTime = -1, wantedBuses = ['all']):
	dts = [] #difference in times
	res = [] #results
	cTime = strftime("%H:%M", localtime()) #current time
	ch = int(cTime[:2]) #current hours
	cm = int(cTime[3:]) #current minutes

	if wantedBuses != ['all'] or minTime != -1:
		for i in range(0, len(bData)):

			sista2 = bData[i][len(bData[i].strip())-2:]
			if sista2 == 'Nu':
				tt1 = 0
				dts.append(tt1)


			sista3 = bData[i][len(bData[i].strip())-3:]
			if sista3 == 'min':
				tt2 = int(bData[i][len(bData[i].strip())-6:][:3])
				dts.append(tt2)


			sista5 = bData[i][len(bData[i].strip())-5:]
			if sista5[2] == ':':
				h = int(sista5[:2])
				m = int(sista5[3:])
				dm = (60*h + m) - (60*ch + cm) #the amount of minutes to coming departure

				dts.append(dm)

		if wantedBuses != ['all']:
			for i in range(0, len(dts)):
				iliner = bData[i].find(" ")
				line = int(bData[i][:iliner])


				if dts[i] > minTime-1 and (line in wantedBuses):
					res.append(bData[i])
		else:
			for i in range(0, len(dts)):
				if dts[i] > minTime-1:
					res.append(bData[i])

		return res

	else:
		return bData

def main():

	#Ange vilken hållplats / station du vill titta avgångstider för, API:et gör en automatisk sökning åt dig:
	sttn = 'Teknis'

	#Ange vilka farkoster du vill se utav:
	#            Buses,Metro, Trains, Trams, Ships
	farkoster = [True, True,  True,   True,  True]

	#Ange om du vill se aktuell störningsinfo eller inte:
	storInfo = False

	#Ange inom hur stort tidspan du vill se lokaltrafiken från 1 till 60 min:
	dt = 60

	#Minimum amount of time for a transport to show on the board:
	minTime = 5

	#input which bus lines you would like to be displayed, if all enter ['all']
	wantedBuses = [4, 6, 67, 72]
	#wantedBuses = ['all']

	#initialising data:
	n = 0
	t = 0
	firebaseText = ''
	[buses, metro, trains, trams, ships, stt] = displayTimes(sttn, farkoster, storInfo, dt)

	#Refresh and update rates:
	st = 0.25 #sleeptime / refreshrate. 1/st must give a whole number
	updt = 5 #how often, in seconds, the board should get info from SL API and firebase


	n = n+1 #constantly increase n by one
	nt =  1 #n%(updt/st) #take n remainder updt/st. For updt=5 and st = 0.25 nt=n%20 and because each loop takes around 0.25 seconds it runs nt==1 once every 5 (updt) seconds. Roughly
	#time.sleep(st)
	if nt == 1:
		try:
			[buses, metro, trains, trams, ships, stt] = displayTimes(sttn, farkoster, storInfo, dt)
			firebaseText = getFireBase()

		except Exception, error:
			print error #prints the error so we can read later what errors have occured

	t = strftime("%Y-%m-%d %H:%M:%S", localtime()) #time needs to be updated quickly so that it doesnt look clunky
	printOnScreen(filterBuses(buses, minTime, wantedBuses), sortMetro(metro, minTime), trains, trams, ships, stt, t, firebaseText)

if __name__ == '__main__':
    main()
