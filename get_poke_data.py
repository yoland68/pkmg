"""Imports data from pokemon api and create json with desirable format"""

import requests
import requests_cache
import json
import re
from collections import deque
import logging

TYPE_API_URL = 'http://pokeapi.co/api/v2/type/'
TYPE_JSON_FILE = './local_json/type.json'
TYPE_URL_PATTERN = re.compile(r'http://pokeapi.co/api/v2/type/(\d+)/')

POKEMON_API_URL = 'http://pokeapi.co/api/v2/pokemon/%d/'
POKEMON_SPECIES_PATTERN = re.compile(r'http://pokeapi.co/api/v2/pokemon-species/(\d+)/')

EVOLUTION_API_URL = 'http://pokeapi.co/api/v2/evolution-chain/%d/'
EVOLUTION_JSON_FILE = './local_json/evolution.json'
EVOLUTION_CHAIN_PATTERN = re.compile(r'http://pokeapi.co/api/v2/evolution-chain/(\d+)/')

MOVE_API_URL = 'http://pokeapi.co/api/v2/move/%d/'
MOVE_URL_PATTERN = re.compile(r'http://pokeapi.co/api/v2/move/(\d+)/')

requests_cache.install_cache('demo_cache')


def _GetId(url, pattern):
  match_result = re.match(pattern, url)
  if match_result is None:
    raise Exception('Invalid input excpetion')
  return int(match_result.group(1))

def EvolutionImport(api_url, evolution_json_file):
  evolution_list = []
  for evo_chain_id in range(1, 79):
    req = requests.get(EVOLUTION_API_URL % evo_chain_id)
    result = req.json().get('chain')
    pokemon_list = []
    pokemon_queue = deque()
    pokemon_queue.append(result)
    while pokemon_queue:
      pokemon = pokemon_queue.popleft()
      species_info = pokemon.get('species')
      pokemon_list.append(
          _GetId(species_info.get('url'), POKEMON_SPECIES_PATTERN))
      if pokemon.get('evolves_to'):
        for i in pokemon.get('evolves_to'):
          pokemon_queue.append(i)
    evolution_list.append({'id': evo_chain_id, 'pokemon_keys': pokemon_list})
  _WriteToFile(EVOLUTION_JSON_FILE, json.dumps(evolution_list))


def PokemonAndMoveImport(api_url, pokemon_json_file, move_json_file):
  pokemon_list = []
  move_id_list = []
  evolution_pair_list = []

  for poke_id in range(1, 152):
    url = api_url % poke_id
    print('requesting for pokemon api: %s' % url)
    poke_req = requests.get(url)
    result = poke_req.json()
    species_url = result.get('species').get('url')
    print('requesting for species api: %s' % species_url)
    poke_species_req = requests.get(species_url)
    species_result = poke_species_req.json()
    if species_result.get('evolves_from_species'):
      evolves_from_id = _GetId(
          species_result.get('evolves_from_species').get('url'), POKEMON_SPECIES_PATTERN)
      if evolves_from_id <= 151:
        evolution_pair_list.append((evolves_from_id, poke_id))
    
    current_move_id_list = []
    for m in result.get('moves'):
      version_group_string = json.dumps(m.get('version_group_details'))
      if 'red-blue' in version_group_string or 'yellow' in version_group_string:
        current_move_id_list.append(_GetId(m.get('move').get('url'),
                                           MOVE_URL_PATTERN))
    move_id_list.extend(current_move_id_list)
    pokemon_list.append(
        {
          'id': poke_id,
          'name': result.get('name'),
          'type_keys': [_GetId(t.get('type').get('url'), TYPE_URL_PATTERN) 
                   for t in result.get('types')],
          'evolution_chain': _GetId(species_result.get('evolution_chain').get('url'),
                                    EVOLUTION_CHAIN_PATTERN),
          'move_keys': current_move_id_list,
        })
    
  for a, b in evolution_pair_list:
    if pokemon_list[a-1].get('evolves_into'):
      pokemon_list[a-1].get('evolves_into').append(b)
    else:
      pokemon_list[a-1]['evolves_into'] = [b]
  _WriteToFile(pokemon_json_file, pokemon_list)

  move_id_list = list(set(move_id_list))
  move_id_list.sort()
  move_list = []
  for move_id in move_id_list:
    move_url = MOVE_API_URL % move_id
    print('requesting for move api: %s' % move_url)
    move_req = requests.get(move_url)
    move_req_result = move_req.json()
    move_list.append(
        {
          'id': move_id,
          'name': move_req_result.get('name'),
          'type_key': _GetId(move_req_result.get('type').get('url'), TYPE_URL_PATTERN)
        })
    _WriteToFile(move_json_file, move_list)


def TypeImport(api_url, type_json_file):
  req = requests.get(api_url)
  import_dic = req.json()
  results = import_dic.get('results')
  output_dic = []
  for i in results:
    type_id = _GetPokemonId(i.get('url'), TYPE_URL_PATTERN)
    type_name = i.get('name')
    assert type_id is not None
    assert type_name is not None
    output_dic.append({'id': type_id, 'name': type_name})
  _WriteToFile(type_json_file, output_dic)

def _WriteToFile(file_name, obj):
  with open(file_name, 'w') as f:
    f.write(json.dumps(obj))

def main():
  # ImportTypes(TYPE_API_URL, TYPE_JSON_FILE)
  # EvolutionImport(EVOLUTION_API_URL, EVOLUTION_JSON_FILE)
  PokemonAndMoveImport(POKEMON_API_URL, 'local_json/pokemon.json', 'local_json/move.json')

if __name__ == '__main__':
  main()
  
