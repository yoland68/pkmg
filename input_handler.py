"""This handler is for create model instance with json input"""
import flask
import logging

import models
import util

app = flask.Flask(__name__)

@app.route('/input/<string:model_type>', methods=['GET', 'POST'])
def InputJson(model_type):
  if flask.request.method == 'GET':
    return flask.render_template('input.html')
  elif flask.request.method == 'POST':
    input_data = flask.request.form 
    model_class = util.CLASS_MAP.get(model_type)
    if model_class is None:
      logging.error('model type: %s, is not found', model_type)
      flask.abort(404)
    model_class.deserialize(input_data)
    return flask.redirect('/')
