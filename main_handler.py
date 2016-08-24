"""This is the main handler to list all the pokemons"""

import flask
import models
import logging
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja_filters
import util

app = flask.Flask(__name__)

jinja_filters.AddJinjaFilteres(app)

@app.route('/')
def MainView():
  pokemon_entities = models.Pokemon.query().fetch()
  pokemons = [p.to_dict() for p in pokemon_entities]
  return flask.render_template('pokemons.html', pokemons=pokemons)

@app.route('/pokemon/<int:pokemon_id>')
def PokemonDetailView(pokemon_id):
  pokemon_entity = models.Pokemon.get_by_id(pokemon_id)
  if pokemon_entity is not None:
    evo_key_map, evo_pokemon_map = util.CreateEvolutionInfo(pokemon_entity)
    pokemon = pokemon_entity.to_dict()
    return flask.render_template(
        'pokemon_detail.html', pokemon=pokemon, evo_key_map=evo_key_map,
        evo_pokemon_map=evo_pokemon_map)
  else:
    flask.abort(404)

@app.route('/report', methods=['GET'])
def ReportGetView():
  return flask.render_template('report.html')

@app.route('/report', methods=['POST'])
def ReportPostView():
  req = flask.request.form
  user = users.get_current_user()
  if user:
    trainer = models.Trainer.get_or_insert(user.user_id())
    if 12 in trainer.want_list:
      return flask.make_response('removed from list')
    else:
      trainer.want_list.append(ndb.Key(models.Pokemon, 12))
      trainer.put()
      return flask.make_response('added to the list')
  else:
    url = users.create_login_url(flask.request.url)
    return flask.redirect(url)

