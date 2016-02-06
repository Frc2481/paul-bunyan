import sys
import copy

files = sys.argv[1:]

for file in files:
	#Do one pass through the file to read last line only, which contains all keys ever seen
	logFile = open(file, 'r')
	line = ""
	for line in logFile:
		pass
	keys = line[8:].split('|')
	logFile.close()
	
	dataMap = {}
	
	#Now write the output
	convertedFile = open(file[:-4]+"-converted.csv",'w')
	headerStr = ""
	for k in keys:
		headerStr += k + ","
	headerStr = headerStr[:-1]
	convertedFile.write(headerStr)
	
	numEntries = len(keys)
	
	logFile = open(file,'r')
	i = 0
	writeEvery = 20
	for line in logFile:
		if line.startswith("KEYLIST-"):
			continue
		if i == 0:
			#Reset data structure to hold all of the data, and insert each key
			dataMap = {}
			for k in keys:
				dataMap[k] = []
		tempkeys = copy.deepcopy(keys)
		line = line[:-2]
		fields = line.split('|')
		for f in fields:
			if len(f.strip()) == 0:
				continue
			#print "'" + f + "'"
			kv = f.split(':')
			k = kv[0]
			v = kv[1]
			dataMap[k].append(v)
			tempkeys.remove(k)
		for remkey in tempkeys:
			dataMap[remkey].append("missing")
		i += 1
		if i >= writeEvery:
			for q in range(i):
				dataStr = '"'
				for k in keys:
					dataStr += dataMap[k][q] + '","'
				dataStr = dataStr[:-2]
				dataStr += "\r\n"
				convertedFile.write(dataStr)
			i = 0
	#Push whatever's left in the dataMap to the file then quit
	for q in range(i):
		dataStr = '"'
		for k in keys:
			dataStr += dataMap[k][q] + '","'
		dataStr = dataStr[:-2]
		dataStr += "\r\n"
		convertedFile.write(dataStr)
	logFile.close()
	convertedFile.close()
