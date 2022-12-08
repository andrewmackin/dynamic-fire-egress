import os
import time
from db import App
import RPi.GPIO as GPIO
# TODO: integrate with api

PIN_LIST = [13,6,5,11,20,21,16,4,3,2,17,27,9,10,22,25,19,26,12]

def init_model():
    GPIO.setmode(GPIO.BCM)
    for pin in PIN_LIST:
      GPIO.setup(pin, GPIO.OUT)
    # init each sign
    nonexit_signs = app.get_sign_ids()
    for id in nonexit_signs:
      path = app.shortest_path(id)
      delta_dir = get_delta_dir(path)
      if get_sign_dir(path) != delta_dir:
        update_signals(app.set_direction(id, delta_dir)[0]['n'])

def get_sign_dir(path):
  return path[0]['path'][0]['dir']
  
def get_delta_dir(path):
  return path[0]['path'][2]['dir']

def on(pin):
  if type(pin) == int and pin > 0:
    GPIO.output(pin, GPIO.HIGH)

def off(pin):
  if type(pin) == int and pin > 0:
    GPIO.output(pin, GPIO.LOW)

def update_signals(node):
  print(node)
  dir = node['dir']
  q1 = node['q1']
  q2 = node['q2']
  q3 = node['q3']
  q4 = node['q4']
  if dir == 'up':
    on(q3), on(q4)
    off(q1), off(q2)
  elif dir == 'down':
    on(q1), on(q2)
    off(q3), off(q4)
  elif dir == 'right':
    on(q3), on(q2)
    off(q1), off(q4)
  elif dir == 'left':
    on(q1), on(q4)
    off(q3), off(q2)
  else: 
    raise AssertionError("invalid direction")

uri = os.environ.get('NEO4J_URI')
user = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')
app = App(uri, user, password)
app.init_db() # TODO: remove for prod
init_model()
time.sleep(30)
app.set_fire(5)
nonexit_signs = app.get_sign_ids()
for id in nonexit_signs:
  path = app.shortest_path(id)
  delta_dir = get_delta_dir(path)
  if get_sign_dir(path) != delta_dir:
    update_signals(app.set_direction(id, delta_dir)[0]['n'])

time.sleep(200)
GPIO.cleanup()
app.close()