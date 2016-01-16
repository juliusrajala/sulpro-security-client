#-*- coding: utf-8 -*-

from flask import Flask, request, redirect
import twilio.twiml
import messenger

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def hello_world():
  resp = twilio.twiml.Response()
  resp.message("Hälytys, tehkää jotain!")
  return str(resp)

def main(active):
  while active:
    print "This loop is active"
    active = False

if __name__ == '__main__':
  active = True
  app.run(debug=True)
  # main(active)