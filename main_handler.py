"""This is the main handler to list all the pokemons"""

import flask
import models
import logging
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja_filters

app = flask.Flask(__name__)

jinja_filters.AddJinjaFilteres(app)


@app.route('/')
def MainView():
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

