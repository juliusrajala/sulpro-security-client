import serial
from threading import Thread

class Serial_listener(Thread):

	

	def __init__(self, callback):
		self.heard = 0
		self.tester = serial.Serial('/dev/ttyACM0', 9600)
		self.is_alert = 0
		self.callback = callback



	def run(self):
		self.listen_now()


	def listen_now(self):

		while True:
			self.heard = self.tester.readline()
			
			if self.heard == 1:
				self.is_alert = self.is_alert +1

			if self.heard != 1:
				self.is_alert = 0

			if self.is_alert == 5:
				self.alert_on()
				break



	def alert_on(self):
		self.callback()


		
	
