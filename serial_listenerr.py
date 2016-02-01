import serial
from threading import Thread

class Serial_listener(object):

	

	def __init__(self, callback):
		self.heard = 0
		self.tester = serial.Serial('/dev/ttyACM0', 9600)
		self.is_alert = 0
                
        self.thread = Thread(target=self.run, args=())
		self.thread.daemon = True                            
		
		#Alempi rivi kusee
		self.callback = callback



	def run(self):
		while True:
			self.heard = self.tester.readline()
			
			if self.heard == 1:
				self.is_alert = self.is_alert +1

			if self.heard != 1:
				self.is_alert = 0

			if self.is_alert == 5:
				self.alert_on()
				breakself.listen_now()


	



	def alert_on(self):
		self.callback()


		
	
