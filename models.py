from google.appengine.ext import ndb
from google.appengine.api import search

import json
import logging

class BaseModel(ndb.Model):
  object_hook = None

  @classmethod
  def deserialize_and_update(cls, data, json_object_hook=None):
    #STUB: this function is for use json to update the database instead of just importing
    pass

  @classmethod
  def deserialize(cls, data, json_object_hook=None):
    if json_object_hook is None:
      json_object_hook = cls.object_hook
    data = json.loads(data.get('json_data'), object_hook=json_object_hook)
    if isinstance(data, list):
      for i in data:
        cls.deserialize_single(i)
    elif isinstance(data, dict):
      cls.deserialize_single(i, data)


  @classmethod
  def deserialize_single(cls, data):
    properties = {}
    for key, value in data.iteritems():
      if getattr(cls, key) is not None:
        properties[key] = value
      else:
        logging.warn('This key: %s does not exist for %s', key, cls.__name__)
    # import pdb
    # pdb.set_trace()
    entity = cls(**properties)
    entity.put()


class Type(BaseModel):
  id = ndb.IntegerProperty(required=True)
  name = ndb.StringProperty(required=True)

  def to_dict(self):
    return {
        'id': self.id,
        'name': self.name
    }


class Pokemon(BaseModel):
  id = ndb.IntegerProperty(required=True, indexed=True)
  name = ndb.StringProperty(required=True, indexed=True)
  evolution_chain = ndb.KeyProperty(kind='Evolution', required=True)
  locations = ndb.GeoPtProperty(repeated=True)
  seen_count = ndb.IntegerProperty(indexed=True)
  want_count = ndb.IntegerProperty(indexed=True)
  have_count = ndb.IntegerProperty(indexed=True)
  type_keys = ndb.KeyProperty(kind='Type', repeated=True)
  evolves_into = ndb.KeyProperty(kind='Pokemon', repeated=True)
  move_keys = ndb.KeyProperty(kind='Move', repeated=True)
  evolution_candy_amount = ndb.IntegerProperty(indexed=False)

  def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'evolution_chain': self.evolution_chain,
        'locations': self.locations,
        'seen_count': self.seen_count,
        'want_count': self.want_count,
        'have_count': self.have_count,
        'type_keys': self.type_keys,
        'evolves_into': self.evolves_into,
        'move_keys': self.move_keys,
        'evolution_candy_amount': self.evolution_candy_amount,
   }

  @staticmethod
  def object_hook(dct):
    if dct.get('locations') is not None and len(dct.get('locations')) != 0:
      geo_pt_list = [search.GeoField(lat, lon) for lac, lon in dct.get('locations')]
      dct.update({'location': geo_pt_list})
    if dct.get('type_keys') is not None and len(dct.get('type_keys')) != 0:
      key_list = [ndb.Key('Type', k) for k in dct.get('type_keys')]
      dct.update({'type_keys': key_list})
    if dct.get('move_keys') is not None and len(dct.get('move_keys')) != 0:
      move_list = [ndb.Key('Move', m) for m in dct.get('move_keys')]
      dct.update({'move_keys': move_list})
    if dct.get('evolution_chain') is not None:
      evolution_id = dct.get('evolution_chain')
      dct.update({'evolution_chain': ndb.Key('Evolution', evolution_id)})
    if dct.get('evolves_into') is not None:
      evo_into_keys = [ndb.Key('Pokemon', p) for p in dct.get('evolves_into')]
      dct.update({'evolves_into': evo_into_keys})
    return dct


class Evolution(BaseModel):
  id = ndb.IntegerProperty(required=True, indexed=True)
  pokemon_keys = ndb.KeyProperty(kind='Pokemon', repeated=True)

  def to_dict(self):
    return {
        'id': self.id,
        'pokemon_keys': self.pokemon_keys
    }

  @staticmethod
  def object_hook(dct):
    if dct.get('pokemon_keys') is not None and len(dct.get('pokemon_keys')) != 0:
      pokemon_list = []
      for poke in dct.get('pokemon_keys'):
        pokemon_list.append(ndb.Key('Pokemon', poke))
      dct.update({'pokemon_keys': pokemon_list})
    return dct

 
class Move(BaseModel):
  id = ndb.IntegerProperty(required=True)
  name = ndb.StringProperty(required=True)
  type_key = ndb.KeyProperty(kind='Type', required=True)

  @staticmethod
  def object_hook(dct):
    if dct.get('type_key') is not None:
      dct.update({'type_key': ndb.Key('Type', dct.get('type_key'))})
    return dct


class Report(BaseModel):
  datetime = ndb.DateTimeProperty(required=True)
  location = ndb.GeoPtProperty()
  pokemon_key = ndb.KeyProperty(kind='Pokemon', required=True)

  def to_dict(self):
    return {
        'datetime': self.datetime,
        'location': self.location,
   }

  @staticmethod
  def object_hook(dct):
    if dct.get('location') is not None:
      dct.update({'type_key': ndb.Key('Type', dct.get('type_key'))})
    return dct


class Trainer(BaseModel):
  id = ndb.StringProperty(required=True)
  want_list = ndb.KeyProperty(kind='Pokemon', repeated=True)
  seen_list = ndb.KeyProperty(kind='Pokemon', repeated=True)
  have_list = ndb.KeyProperty(kind='Pokemon', repeated=True)

  def to_dict(self):
    return {
        'id': self.id,
        'reports': self.reports,
        'want_list': self.want_list,
        'seen_list': self.seen_list,
        'have_list': self.have_list
    }

  @staticmethod
  def object_hook(dct):
    if dct.get('seen_list') is not None and len(dct.get('seen_list')) != 0:
      seen_list = []  
      for i in dct.get('seen_list'):
        seen_list.append(ndb.Key('Pokemon', i))
      dct.update({'seen_list': seen_list})
    if dct.get('want_list') is not None and len(dct.get('want_list')) != 0:
      want_list = []  
      for i in dct.get('want_list'):
        have_list.append(ndb.Key('Pokemon', i))
      dct.update({'want_list': want_list})
    if dct.get('have_list') is not None and len(dct.get('have_list')) != 0:
      have_list = []  
      for i in dct.get('have_list'):
        have_list.append(ndb.Key('Pokemon', i))
      dct.update({'have_list': have_list})

    return dct
