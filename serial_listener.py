import serial

tester = serial.Serial('COM19', 9600)

heard = 0

while True:
	#heard = tester.readline()
	print tester.readline()
	if heard == 1:
		print heard
	
