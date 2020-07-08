import requests

url = "https://www.pokemon.com/us/api/pokedex/kalos"
r = requests.get(url)
print("Status code:", r.status_code)

response_dict = r.json()

pokemons = []
urls = []
dict = {}

# Creates a dictionary with numbers as keys
for i in range(1, 891):
    dict[i] = {}

# Stores the name of pokemon in a list called pokemons
# This way, duplicates are ommitted
for item in response_dict:
    if item["name"] not in pokemons:
        pokemons.append(item["name"])
        urls.append(item["ThumbnailImage"])
        
# Passes each pokemon into the dictionary
for key in dict.keys():
    pokemon = pokemons[key-1]
    dict[key]["name"] = pokemon
    pokemon_url = urls[key-1]
    dict[key]["image"] = pokemon_url

