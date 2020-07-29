import requests
import json

url = "https://www.pokemon.com/us/api/pokedex/kalos"
r = requests.get(url)
print("Status code:", r.status_code)

response_dict = r.json()

pokemons = []
urls = []
pokemon_dict = {}
types = []

# Creates a dictionary with numbers as keys
for i in range(1, 722):
    pokemon_dict[i] = {}

# Stores the name of pokemon in a list called pokemons
# This way, duplicates are ommitted
for item in response_dict:
    if item["name"] not in pokemons:
        pokemons.append(item["name"])
        types.append(item["type"])
        urls.append(item["ThumbnailImage"])
        
# Passes each pokemon into the dictionary
for key in pokemon_dict.keys():
    pokemon = pokemons[key-1]
    pokemon_dict[key]["name"] = pokemon
    pokemon_url = urls[key-1]
    pokemon_dict[key]["image"] = pokemon_url
    type1 = types[key-1][0]
    pokemon_dict[key]["type1"] = type1
    if len(types[key-1]) > 1:
        type2 = types[key-1][1]
        pokemon_dict[key]["type2"] = type2


