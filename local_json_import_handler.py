"""Pokemon"""

import os
import re

import flask
import models
import logging
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import taskqueue

import util

app = flask.Flask(__name__)

file_pattern = re.compile(r'.*/(\w+).json')

LOCAL_PATH = '/home/yoland/Code/pkmg'

@app.route('/local-import')
def LocalImport():
  retry_options = taskqueue.TaskRetryOptions(task_retry_limit=0)
  import pdb
  pdb.set_trace()
  if flask.request.args.get('queue_name'):
    queue_name = flask.request.args.get('queue_name')
  else:
    queue_name = 'default'
  taskqueue.add(url='/local-import/worker',
                queue_name=queue_name,
                method='GET', retry_options=retry_options)
  return 'Done!'

@app.route('/local-import/worker')
def LocalImportWoker():
  local_json_dir = os.path.abspath(os.path.join(LOCAL_PATH, 'local_json'))
  assert os.path.isdir(local_json_dir)
  json_file_list = [os.path.join(local_json_dir, f) for f in
      os.listdir(local_json_dir) if f.endswith('.json') and
      os.path.isfile(os.path.join(local_json_dir, f))]
  for file_path in json_file_list:
    try:
      type_match_result = file_pattern.match(file_path)
      if type_match_result is None:
        logging.warn('File does not match any type: %s', file_path)
        continue
      model_type_name = type_match_result.group(1)
      model_class = util.CLASS_MAP.get(model_type_name, None)
      if model_class is not None:
        ndb.delete_multi(model_class.query().fetch(keys_only=True))
        with open(file_path, 'r') as f:
          model_class.deserialize(f.read())
    except Exception as e:
      logging.error('Failed importing %s', file_path)
      raise

  return 'Finished!'
