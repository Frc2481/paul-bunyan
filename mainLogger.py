#Install python 2.7, then execute "pip install pynetworktables".  Then this should work

import sys
import time, datetime
import os
from networktables import NetworkTable

if not os.path.exists("/media/TOM/2481.txt"):
	#USB drive not detected
	print "No usb drive detected."
	sys.exit(0)

import logging
logging.basicConfig(level=logging.DEBUG)

#Constants
keysToIgnore = ["Kp","Auto Chooser/options","Auto Modes/options"]
for k in range(len(keysToIgnore)):
	keysToIgnore[k] = "/SmartDashboard/" + keysToIgnore[k]
ip = "roboRIO-2481-FRC.local"
keysToIgnoreSet = set(keysToIgnore)
loopsPerFlush = 500 #Assume we log at 50 Hz, with a flush every 10 seconds.  50 loops/second * 10 seconds/flush = 500 loops/flush

#Set up the network table
NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

#File setup
#First set how many bytes are buffered before a file flush.  0 is unbuffered, 1 is line buffered, negative is system default.
#We want it large enough that manual flushing will activate before the buffer fills up, but not so large as to use up all the coprocessor's memory
bufsize = 1048576 #?  Experimentation needed
fnDateTime = datetime.datetime.now().strftime("%m.%d.%Y-%H.%M.%S")
logFile = open("/media/TOM/logFile-" + fnDateTime + ".csv", 'w', bufsize)

matchOver = False #If this ever goes true we're about to shut down.  Do a final write and start the shutdown sequence

q=0
i = 0
keyDict = {}
while not matchOver and q<10000000:
	print q
	sdTable = NetworkTable.getTable("SmartDashboard")
	logTable = NetworkTable.getTable("2481/log_table")
	#Get the list of keys currently in the table
	sdtableKeysList = sdTable.node.entryStore.keys()
	logtableKeysList = logTable.node.entryStore.keys()
	for keyIter in range(len(sdtableKeysList)):
		sdtableKeysList[keyIter] = str(sdtableKeysList[keyIter])
	for keyIter in range(len(logtableKeysList)):
		logtableKeysList[keyIter] = str(logtableKeysList[keyIter])
	sdtableKeys = set(sdtableKeysList)
	logtableKeys = set(logtableKeysList)
	#Subtract off the blacklisted "meta" keys to get a list of keys we are interested in
	sdkeysToLog = sdtableKeys.difference(keysToIgnoreSet)
	logkeysToLog = logtableKeys.difference(keysToIgnoreSet)
	#Iterate over every remaining key and push its value onto a string
	entryStr = ""
	if len(sdkeysToLog) > 0 or len(logkeysToLog) > 0:
		for key in sdkeysToLog:
			if not key.startswith("/SmartDashboard/"):
				continue
			if "~TYPE~" in key:
				continue
			if "/name" in key:
				continue
			subkey = key[16:]
			val = str(sdTable.getValue(str(subkey),"missing"))
			entryStr += str(subkey) + ":" + val + "|"
			keyDict[subkey] = 0
			if subkey == "matchOver" and val == "true":
				matchOver = True
		for key in logkeysToLog:
			if not key.startswith("/2481/log_table/"):
				continue
			if "~TYPE~" in key:
				continue
			in "/name" in key:
				continue
			subkey = key[16:]
			val = str(logTable.getValue(str(subkey),"missing"))
			entryStr += str(subkey) + ":" + val + "|"
			keyDict[subkey] = 0
		entryStr = entryStr[:-1]
		entryStr += "\r\n"
		logFile.write(entryStr)
		#print "Wrote a line of data."
		if i >= loopsPerFlush:
			logFile.flush()
			os.fsync(logFile.fileno())
			#print "Flushed!"
			i = 0
		else:
			i += 1
	time.sleep(0.02)
        q += 1
	
#Put out one final line with all the keys seen
keyStr = "KEYLIST-"
for k in keyDict.keys():
	keyStr += k + "|"
keyStr = keyStr[:-1]
logFile.write(keyStr)
	
#If we get here, matchOver went True.  Time to shut down
logFile.flush()
os.fsync(logFile.fileno())
logFile.close()

print "DONE!"
#Shut down the coprocessor.  Requires admin privileges
os.system("shutdown -P now")
