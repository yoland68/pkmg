import jinja2

def ConvertToImageName(pokemon_id):
  return "%03d" % pokemon_id

def AddJinjaFilteres(app):
  filters = app.jinja_env.filters
  filters['ConvertToImageName'] = ConvertToImageName
