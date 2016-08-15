import jinja2
from jinja2 import evalcontextfilter, Markup, escape

_EVO_TEMPLATE = '<span>%s</span>'

_EVO_TEMPLATE_END = ''

def ConvertToImageName(pokemon_id):
  return '%03d' % pokemon_id

@evalcontextfilter
def ConstEvoChain(eval_ctx, evo_key_map, evo_pokemon_map, current_id):
  td_template = '<td evolve-into="{0}" class="{3}"><a href="/pokemon/{1}"><img src="/static/imgs/pokemon/{1}.png">{2}</a></td>'
  table_template = '<table><tbody><tr>%s</tr></tbody></table>'
  xs = []
  for k, v in sorted(evo_key_map.items(), key=lambda t: t[0]):
    current = 'current' if k == current_id else ''
    xs.append(td_template.format(
        escape(' '.join(str(i) for i in v)),
        escape(ConvertToImageName(k)),
        escape(evo_pokemon_map[k].name),
        current))
  result = '<table><tbody><tr>%s</tr></tbody></table>' % ''.join(xs)
  if eval_ctx.autoescape:
    result = Markup(result)
  return result

def AddJinjaFilteres(app):
  filters = app.jinja_env.filters
  filters['ConvertToImageName'] = ConvertToImageName
  filters['ConstEvoChain'] = ConstEvoChain


