from google.appengine.ext import ndb

class Type(ndb.Model):
  type_id = ndb.IntegerProperty(required=True)
  name = ndb.StringProperty(required=True)

  def to_dict(self):
    return {
        'type_id': self.type_id,
        'name': self.name
    }

class Pokemon(ndb.Model):
  pokemon_id = ndb.IntegerProperty(required=True, indexed=True)
  name = ndb.StringProperty(required=True, indexed=True)
  evolution = ndb.JsonProperty(required=True)
  locations = ndb.GeoPtProperty(repeated=True)
  seen_count = ndb.IntegerProperty(indexed=True)
  want_count = ndb.IntegerProperty(indexed=True)
  have_count = ndb.IntegerProperty(indexed=True)
  evolution_candy_amount = ndb.IntegerProperty(indexed=False)
  types = ndb.StructuredProperty(Type, repeated=True)

  def to_dict(self):
    return {
        'pokemon_id': self.pokemon_id,
        'name': self.name,
        'evolution': self.evolution,
        'locations': self.locations, #how to serialize this one?
        'seen_count': self.seen_count,
        'want_count': self.want_count,
        'have_count': self.have_count,
        'evolution_candy_amount': self.evolution_candy_amount,
        'types': self.types
    }
 
class Report(ndb.Model):
  datetime = ndb.DateTimeProperty(required=True)
  location = ndb.GeoPtProperty()
  user_id = ndb.StringProperty(required=True)
  pokemon_id = ndb.StringProperty(required=True)

  def to_dict(self):
    return {
        'datetime': self.datetime,
        'location': self.location,
        'user_id': self.user_id,
        'pokemon_id': self.pokemon_id
   }

class Trainer(ndb.Model):
  user_id = ndb.StringProperty(required=True)
  reports = ndb.StructuredProperty(Report, repeated=True)
  want_list = ndb.IntegerProperty(repeated=True)
  seen_list = ndb.IntegerProperty(repeated=True)
  have_list = ndb.IntegerProperty(repeated=True)

  def to_dict(self):
    return {
        'user_id': 'user_id',
        'reports': 'reports',
        'want_list': 'want_list',
        'seen_list': 'seen_list',
        'have_list': 'have_list'
    }


