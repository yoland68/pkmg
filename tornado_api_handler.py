"""This is a dev handler where it displays the info about the database"""

import flask
import logging

from pprint import pprint
import json

import models
import util

app = flask.Flask(__name__)
app.json_encoder = util.ModelJSONEncoder

@app.route('/api/<string:model_type>/single')
def ApiSingle(model_type):
  model_class = util.CLASS_MAP.get(model_type)
  if len(flask.request.args) < 1:
    logging.error('need request argument for single instance query')
    flask.abort(404) 
  args = flask.request.args.items()
  try:
    properties = [];
    for key, val in args:
      if key == 'id':
        result = model_class.get_by_id(int(val))
        break
      else:
        properties.append(getattr(model_class, key) == val)
        result = model_class.query(*properties).get()
    if result is None:
      logging.error('%s result does not exist', model_class._class_name())
      flask.abort(404)
    result_dict = result.to_dict()
    if isinstance(result, models.Pokemon):
      evo_key_map, evo_pokemon_map = util.CreateEvolutionInfo(result)
      result_dict['evo_key_map'] = evo_key_map
      result_dict['evo_pokemon_map'] = evo_pokemon_map
    return flask.jsonify(result_dict)
  except AttributeError as e:
    logging.error("Error: %s", e)
    flask.abort(404)

@app.route('/api/<string:model_type>/all')
def ApiAll(model_type):
  model_class = util.CLASS_MAP.get(model_type)
  if model_class is None:
    logging.error('Model type "%s" not found', model_type)
    flask.abort(404)
  results = model_class.query().fetch()
  results_dict = [i.to_dict() for i in results]
  return flask.jsonify({"results": results_dict})
