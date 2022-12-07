import os
from db import App
# TODO: integrate with api

def get_sign_dir(path):
  print()
  return path[0]['path'][0]['dir']
def get_delta_dir(path):
  return path[0]['path'][2]['dir']

ALARM_ID = 5 # will be input to api
uri = os.environ.get('NEO4J_URI')
user = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')
app = App(uri, user, password)
app.init_db() # TODO: remove for prod
app.set_fire(ALARM_ID)
nonexit_signs = app.get_sign_ids()
for id in nonexit_signs:
  path = app.shortest_path(id)
  if get_sign_dir(path) != get_delta_dir(path):
    print("detected") # send signal to appropriate sign, update history

app.close()