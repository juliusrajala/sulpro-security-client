import sys
import socket
import datetime
from time import gmtime, strftime
from messenger import Messenger
from serial_listener import Serial_listener

import time
try:
  import RPi.GPIO as GPIO
except:
  print "Likely not using raspberry pi"
  pass

class controller(object):
  def __init__(self):
    self.con = socket.socket()
    self.messenger = Messenger()
    self.listener = Serial_listener(self.alert())
    
    #Variables to display uptime etc.
    self.online_from = strftime("%d-%m-%Y %H:%M:%S")
    self.alert_since = ""
    self.last_danger = ""
    
    #Different states of the controller
    self.alert = False
    self.active = True
    self.danger = False

    #IRC - Connection - Specs
    self.HOST = "irc.utu.fi"
    self.PORT = 6667
    self.PASSWORD = ""
    self.NICK = "SecurityOfficerRobot"
    self.IDENTITY = self.NICK
    self.REALNAME = "SORROBOTTI123"
    self.CHANNELINIT = "#securityofficerobot"
    self.OWNER = "Lorenz0"
    self.END = "\r\n"
    

  def translate(self, data):
    print data
    #Different chat commands
    command_dictionary = {
      "PING": self.ping_response,
      "!OK" : self.handle_alert,
      "!ON" : self.start_watching,
      "!OF" : self.stop_watching,
      "!EX" : self.exit,
      "!ST" : self.get_status
    }
    message = data.split(" ")
    if message[0] == "PING":
      print message
      self.ping_response(message[1])
      return
    if self.CHANNELINIT in message:
      print "Message to robot."
      query = message[len(message)-1]
      print query
      if query[0] == ':':
        query = query.translate(None, ':')
        query = query[:3]
        print query
        print len(query)
      if query in command_dictionary:
        print "Query found in dictionary"
        command_dictionary[query]()

  def ping_response(self, extra):
    print "PONG " + extra.split(":")[1]
    print extra
    self.con.send("PONG "+ self.HOST +" "+ extra.split(":")[1]+self.END)

  def exit(self):
    print "Shutting things down."
    self.con.close()
    self.active = False

  def handle_alert(self):
    print "Handling an alert."
    self.danger = False
    self.messenger.send_message("The alert was cancelled at: "+ strftime("%d-%m-%Y %H:%M:%S"))

  def stop_watching(self):
    print "Going to sleep and dream about things that don't scare me."
    self.alert = False
    self.danger = False;

  def start_watching(self):
    self.alert_since = strftime("%d-%m-%Y %H:%M:%S")
    print "Going into watch-dog mode."
    self.alert = True
    self.alertMode()

  def get_status(self):
    print "Sending status messages"
    self.con.send("PRIVMSG "+self.CHANNELINIT+ " :" + "Server up since: "+self.online_from + self.END)
    self.con.send("PRIVMSG "+self.CHANNELINIT+ " :" + "Alert since: "+self.alert_since + self.END)
    self.con.send("PRIVMSG "+self.CHANNELINIT+ " :" + "Last movement: "+self.last_danger + self.END)

  def alertMode(self):
    self.con.send("PRIVMSG "+self.CHANNELINIT+" :"+ "HLEP, moving things!" + self.END)
    self.last_danger = strftime("%d-%m-%Y %H:%M:%S")
    print "Following data from arduino"
    listener.start()
  
  def alert(self):
      print "Alert, movement detected!"
      self.messenger.send_message("Danger, danger! Movement at: " + strftime("%d-%m-%Y %H:%M:%S"))
      self.danger = True

  def alert_sound(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(22, GPIO.OUT)
    
    bell = GPIO.PWM(22, 1500)
    bell.start(1)
    time.sleep(100)
    bell.start(0)

  def run(self):
    self.con.connect((self.HOST, self.PORT))
    self.con.send("NICK " + self.NICK + self.END)
    self.con.send("USER " + self.IDENTITY + " " + self.HOST +" bla :" +self.REALNAME +self.END)
    self.con.send("JOIN " + self.CHANNELINIT+self.END)

    while self.active:
      if self.danger:
        print "Do something about it, please!"
        try:
          self.alert_sound()
        except:
          print "Alert sound couldn't be called."
      data = self.con.recv(4096)
      self.translate(data)

if __name__ == '__main__':
  ctrl = controller()
  ctrl.run()