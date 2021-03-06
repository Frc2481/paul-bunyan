import cv2
import urllib
import numpy as np
from vision import GoalFinder
from networktables import NetworkTable
import datetime
from time import sleep

from networktables2 import NumberArray
import logging
logging.basicConfig(level=logging.DEBUG)

def main():

    ip = "10.24.81.2"
    NetworkTable.setIPAddress(ip)
    NetworkTable.setClientMode()

    #print "Initializing Network Tables"
    NetworkTable.initialize()

    goalFinder = GoalFinder()
    
    stream = urllib.urlopen('http://10.24.81.11/mjpg/video.mjpg')
    bytes = ''

    #print "Start Target Search Loop..."
    #turn true for single picture debuging
    first = False
    
    beagle = NetworkTable.getTable("GRIP")
    goals_table = beagle.getSubTable("aGoalContours")
    
    while True:
	
        #TODO: Fetch image from camera.
        # img = cv2.imread("0.jpg")
        bytes += stream.read(16384)
        b = bytes.rfind('\xff\xd9')
        a = bytes.rfind('\xff\xd8', 0, b-1)
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            img = cv2.imdecode(np.fromstring(jpg, dtype = np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
            goalFinder.process_image(img)

            goals_table.putValue("centerX", NumberArray.from_list(goalFinder.targetXs))
            goals_table.putValue("centerY", NumberArray.from_list(goalFinder.targetYs))
            goals_table.putValue("width", NumberArray.from_list(goalFinder.targetWidths))
            goals_table.putValue("height", NumberArray.from_list(goalFinder.targetHeights))
            goals_table.putValue("area", NumberArray.from_list(goalFinder.targetAreas))

            #if len(goalFinder.targetAreas) > 0:
            #    print goalFinder.targetAreas

            #Use if you want to the save the image and retrieve it later.
	    if first:
		first = False
	    	cv2.imwrite("test.jpg", img)
	
	goals_table.putNumber("OwlCounter", goals_table.getNumber("OwlCounter", 0) + 1) 

	sleep(.01)


if __name__ == "__main__":
    main()
