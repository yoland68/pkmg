"""This is the main handler to list all the pokemons"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def IndexView():
  return 'hello world! done by Yoland'
