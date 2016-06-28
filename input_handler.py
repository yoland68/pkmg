"""This handler is for create model instance with json input"""
import flask
import logging

import models
import util

app = flask.Flask(__name__)

@app.route('/input/<string:model_type>')
def InputJson(model_type):
  if request.method == 'GET':
    flask.render_template() <===== HERE!!!!
  input_data = flask.request.form 
  model_class = util.CLASS_MAP.get(model_type)
  if model_class is None:
    logging.error('model type: %s, is not found', model_type)
    flask.abort(404)
  model_class.deserialize(input_data)
