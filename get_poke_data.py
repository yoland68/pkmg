"""Imports data from pokemon api and create json with desirable format"""

import requests
import json
import re

TYPE_API_URL = 'http://pokeapi.co/api/v2/type/'
TYPE_JSON_FILE = 'type.json'
TYPE_URL_PATTERN = re.compile(r'http://pokeapi.co/api/v2/type/(\d+)/')

def ImportTypes(api_url):
  req = requests.get(api_url)
  import_dic = req.json()
  results = import_dic.get('results')
  output_dic = []
  for i in results:
    match_result = re.match(TYPE_URL_PATTERN, i.get('url'))
    if match_result is None:
      raise Exception('Invalid input excpetion')
    type_id = match_result.group(1)
    type_name = i.get('name')
    assert type_id is not None
    assert type_name is not None
    output_dic.append({'id': type_id, 'name': type_name})
  return json.dumps(output_dic)

def main():
  json_string = ImportTypes(TYPE_API_URL, )
  with open(TYPE_JSON_FILE, 'w') as f:
    f.write(json_string)

if __name__ == '__main__':
  main()
  
