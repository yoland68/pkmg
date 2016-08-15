from google.appengine.ext import ndb
import collections

from flask.json import JSONEncoder

import models

CLASS_MAP = {
    'pokemon': models.Pokemon,
    'trainer': models.Trainer,
    'report': models.Report,
    'type': models.Type,
    'evolution': models.Evolution,
    'move': models.Move,
}

class ModelJSONEncoder(JSONEncoder):
  def default(self, obj):
    try:
      if isinstance(obj, ndb.Key):
        obj = obj.get()
        if hasattr(obj, 'name'):
          return obj.name
        return str(obj)
      if isinstance(obj, ndb.Model):
        if hasattr(obj, 'name'):
          return obj.name
        return str(obj)
      iterable = iter(obj)
    except TypeError:
      pass
    else:
      return list(iterable)
    return JSONEncoder.default(self, obj)
    
def CreateEvolutionInfo(pokemon_entity):
  return ExtractEvolutionInfo(pokemon_entity.evolution_chain_key.get())

def ExtractEvolutionInfo(evolution_entity):
  key_map = {}
  pokemon_map = {}
  for k in evolution_entity.pokemon_keys:
    p = k.get()
    pokemon_map[k.id()] = p
    key_map[k.id()] = [i.id() for i in p.evolves_into]
  return key_map, pokemon_map
