from google.appengine.ext import ndb

import util

class Pokemon(ndb.Model):
  pokemon_id = ndb.IntegerProperty(required=True, indexed=True)
  name = ndb.StringProperty(required=True, indexed=True)
  evolution = ndb.JsonProperty(required=True)
  locations = ndb.GeoPtProperty(repeated=True)
  seen_count = ndb.IntegerProperty(indexed=True)
  want_count = ndb.IntegerProperty(indexed=True)
  have_count = ndb.IntegerProperty(indexed=True)
  evolution_candy_amount = ndb.IntegerProperty()

  def to_dict(self):
    return {
        'pokemon_id': self.pokemon_id,
        'name': self.name,
        'evolution': self.evolution,
        'locations': self.locations, #how to serialize this one?
        seen_count
        want_count
        have_count


class Type(ndb.Model):
  type_id = ndb.IntegerProperty(required=True)
  name = ndb.StringProperty(required=True)
  
class Trainer(ndb.Model):
  user_id = ndb.StringProperty(required=True)
  reports = ndb.StructureProperty(Report, repeated=True)
  want_list = ndb.IntegerProperty(repeated=True)
  seen_list = ndb.IntegerProperty(repeated=True)
  have_list = ndb.IntegerProperty(repeated=True)

class Report(ndb.Model):
  datetime = ndb.DateTimeProperty(required=True)
  location = ndb.GeoPtProperty()
  user_id = ndb.StringProperty(required=True)
  pokemon_id = ndb.StringProperty(required=True)
