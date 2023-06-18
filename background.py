from flask import Flask
from flask import request
from threading import Thread
import os
import time


app = Flask('')

@app.route('/')
def home():
  return "Sup, homie"

def run():
  app.run(host = '0.0.0.0', port = os.getenv('PORT', default=3000))

def keep_alive():
  t = Thread(target=run)
  t.start()
