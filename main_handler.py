"""This is the main handler to list all the pokemons"""

import flask
import models
import logging
from google.appengine.api import users

app = flask.Flask(__name__)


@app.route('/')
def IndexView():
  return 'hello world! done by Yoland'

@app.route('/pokemon')
def PokemonView():
  pokemon_entities = models.Pokemon.query().fetch()
  pokemons = [p.to_dict() for p in pokemon_entities]
  return flask.render_template('pokemons.html', pokemons=pokemons)

@app.route('/report', methods=['GET'])
def ReportGetView():
  return flask.render_template('report.html')

@app.route('/report', methods=['POST'])
def ReportPostView():
  req = flask.request.form
  user = users.get_current_user()
  if user:
    print('###YOLAND###: user_id %s' % user.user_id())
    trainer = models.Trainer.get_or_insert(user.user_id())
    if 12 in trainer.want_list:
      return flask.make_response('removed from list')
    else:
      return flask.make_response('added to the list')
  else:
    print('###YOLAND###: %s' % flask.request.url)
    url = users.create_login_url(flask.request.url)
    return flask.redirect(url)

