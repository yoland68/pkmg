"""This is the main handler to list all the pokemons"""

import flask
import models

app = flask.Flask(__name__)


@app.route('/')
def IndexView():
  return 'hello world! done by Yoland'

@app.route('/pokemon')
def PokemonView():
  pokemon_entities = models.Pokemon.query().order(models.Pokemon.id).fetch()
  pokemons = [p.to_dict() for p in pokemon_entities]
  return flask.render_template('pokemons.html', pokemons=pokemons)
