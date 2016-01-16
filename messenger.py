#-*- coding: utf-8 -*-
import settings as keys
import number
from twilio.rest import TwilioRestClient


class Messenger(object):
  def __init__(self):
    #Blah blah
    print "Initializing app class"
    self.active = True
    #Initializing twilio keys.
    try:
      self.twilio_id = keys.twilio_sid
      self.twilio_secret=keys.twilio_secret
      print "Keys initialized"
    except:
      print "Key initialization failed, closing application"
      self.active = False
    #Initializing Client next
    try:
      self.client = TwilioRestClient(self.twilio_id, self.twilio_secret)
    except:
      print "Client initialization failed."

  def send_message(self, message):
    try:
      message = self.client.messages.create(
        body = message,
        to = number.alert_number,
        from_ = number.twilio_number
        )
      print message.sid
    except:
      print "Message delivery failed."
      raise

  def main(self):
    #This will be where the main loop lives.
    # self.server.run(debug=True)
    while self.active:
      print "Sending message to Julius"
      message = raw_input("What do you want to send?\r\n")
      self.send_message(message)
      self.active = False
      print "Running the while loop"