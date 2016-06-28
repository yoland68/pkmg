"""This is a dev handler where it displays the info about the database"""

import flask
import logging

import models

app = flask.Flask(__name__)

_CLASS_MAP = {
    'pokemon': models.Pokemon,
    'trainer': models.Trainer,
    'report': models.Report,
    'type': models.Type
}

@app.route('/api/<string:model_type>/single')
def ApiSingle(element):
  model_class = _CLASS_MAP.get(model_type)
  if len(flask.request.args) < 1:
    logging.error('need request argument for single instance query')
    flask.abort(404) 
  first_arg = flask.request.args.popitem()
  try:
    result = model_class.query(getattr(model_class, first_arg[0]) == element)
    return flask.jsonify(result.to_dict())
  except AttributeError as e:
    logging.error("Error: %s", e)
    flask.abort(404)

@app.route('/api/<string:model_type>/all')
def ApiAll(model_type):
  model_class = _CLASS_MAP.get(model_type)
  if model_class is None:
    logging.error('Model type "%s" not found', model_type)
    flask.abort(404)
  results = model_class.query()
  return flask.jsonify([i.to_dict() for i in results])
