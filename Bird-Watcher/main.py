from networktables import NetworkTable
import os
import time

def main():
	prev = 0
	current = 0
	owlMissingCounter = 0
	robotMissingCounter = 0
	prevRobotMissing = 0
	currentRobotMissing = 0

	ip = "roboRIO-2481-FRC.local"
	NetworkTable.setIPAddress(ip)
    	NetworkTable.setClientMode()
	
	print "Bird Watcher: Initializing Network Tables"
	NetworkTable.initialize()
	
	time.sleep(2)
	
	while True:
		beagle = NetworkTable.getTable("GRIP")
        	goals_table = beagle.getSubTable("aGoalContours")
		current = goals_table.getNumber("OwlCounter", 0)
		currentRobotMissing = goals_table.getNumber("RobotCounter", 0)
		if current == prev:
			owlMissingCounter += 1
		else:
			owlMissingCounter = 0
		
		#print owlMissingCounter
		
		prev = current
		
		if owlMissingCounter > 5:
			print "Bird Watcher: Restarting Owl Service"
			os.system("systemctl restart Camera")
			time.sleep(5)
		else:
			time.sleep(1)

		if currentRobotMissing == prevRobotMissing:
			robotMissingCounter += 1
		else:
			robotMissingCounter = 0
		prevRobotMissing = currentRobotMissing

		if robotMissingCounter > 5:
			print "Robot Watcher: Restarting Owl Service"
			os.system("systemctl restart Camera")
			time.sleep(5)

if __name__ == "__main__":
	main()
