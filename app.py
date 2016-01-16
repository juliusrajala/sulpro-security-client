#-*- coding: utf-8 -*-
import settings as keys

class app(object):
  def __init__(self):
    #Blah blah
    print "Initializing app class"
    self.active = True
    try:
      self.twilio_id = keys.twilio_sid
      self.twilio_secret=keys.twilio_secret
      print "Keys initialized"
    except:
      print "Key initialization failed, closing application"
      self.active = False

  def main(self):
    #This will be where the main loop lives.
    while self.active:
      self.active = False
      print "Running the while loop"


if __name__ == '__main__':
  ourApp = app()
  ourApp.main()