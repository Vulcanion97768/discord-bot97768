import json
import discord
import requests
from math import floor
from pokemon_dictionary import pokemon_dict


def add_experience(user_id):
    with open("pokemon.json") as file:
        data = json.load(file)
        if user_id in data["users"]:
            for pokemon in data["users"][user_id]:
                if pokemon["selected"]:
                    pokemon["exp"] += 15
    with open("pokemon.json", "w") as file:
        json.dump(data, file, indent=4)


def check_experience(user_id):
    with open("pokemon.json") as file:
        data = json.load(file)
    if user_id in data["users"]:
        for pokemon in data["users"][user_id]:
            if pokemon["selected"]:
                needed_exp = int((4 * (pokemon["lvl"]+1)**3) / 5)
                if pokemon["exp"] > needed_exp:
                    pokemon["lvl"] += 1
                    lvl = pokemon["lvl"]
                    name = pokemon["name"]
                    with open("pokemon.json", "w") as file:
                        json.dump(data, file, indent=4)
                    poke_id = return_id(name)
                    evol_active, evolution = check_evolution(poke_id, user_id, name)
                    check_type(poke_id, name, user_id)
                    return evol_active, evolution, True, name, lvl
                elif needed_exp > pokemon["exp"]:
                    return False, "name", False, "name", 17
    else:
        return False, "name", False, None, None


def return_info(args, user_id, data):
    index = int(args[0]) - 1
    name = data["users"][user_id][index]["name"]
    type1 = data["users"][user_id][index]["type1"]
    if "type2" in data["users"][user_id][index]:
        type2 = data["users"][user_id][index]["type2"]
    lvl = data["users"][user_id][index]["lvl"]
    if lvl < 100:
        exp = data["users"][user_id][index]["exp"]
        needed_exp = int((4 * (lvl + 1)** 3) / 5)
    hp_iv = data["users"][user_id][index]["hp_iv"]
    atk_iv = data["users"][user_id][index]["atk_iv"]
    def_iv = data["users"][user_id][index]["def_iv"]
    speed_iv = data["users"][user_id][index]["speed_iv"]
    spatk_iv = data["users"][user_id][index]["spatk_iv"]
    spdef_iv = data["users"][user_id][index]["spdef_iv"]
    nature = data["users"][user_id][index]["nature"]
    title = f"{name}"
    if lvl >= 100:
        description = "\n**Max Level**"
    else:
        description = f"\n**Level:** {lvl} \n{exp}/{needed_exp}"
    if "type2" in locals():
        description += f"\n**Type:** {type1.title()}/{type2.title()}"
    else:
        description += f"\n**Type:** {type1.title()}"
    for key, item in pokemon_dict.items():
        if item["name"] == name:
            image = item["image"]
            poke_id = key

    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    r = requests.get(url)
    response_dict = r.json()
    base_hp = response_dict["stats"][0]["base_stat"]
    base_atk = response_dict["stats"][1]["base_stat"]
    base_def = response_dict["stats"][2]["base_stat"]
    base_speed = response_dict["stats"][5]["base_stat"]
    base_spatk = response_dict["stats"][3]["base_stat"]
    base_spdef = response_dict["stats"][4]["base_stat"]
    hp = int((((2 * base_hp + hp_iv) * lvl) / 100) + lvl + 10)
    url = f"https://pokeapi.co/api/v2/nature/{nature.lower()}/"
    r = requests.get(url)
    response_dict = r.json()

    try:
        decreased = response_dict["decreased_stat"]["name"]
        increased = response_dict["increased_stat"]["name"]
    except TypeError:
        decreased, increased = 1, 1

    base_stats = [base_atk, atk_iv, base_def, def_iv, base_spatk,
                  spatk_iv, base_spdef, spdef_iv, base_speed, speed_iv]
    stats = []
    for i in range(0, 9, 2):
        increased_stat = floor(
            ((((2 * base_stats[i] + base_stats[i+1]) * lvl) / 100) + 5) * 1.1)
        decreased_stat = floor(
            ((((2 * base_stats[i] + base_stats[i+1]) * lvl) / 100) + 5) * .9)
        normal_stat = floor(
            ((((2 * base_stats[i] + base_stats[i+1]) * lvl) / 100) + 5) * 1)
        if increased == 1:
            stat = normal_stat
        elif decreased == "attack" and i == 0:
            stat = decreased_stat
        elif decreased == "defense" and i == 2:
            stat = decreased_stat
        elif decreased == "special-attack" and i == 4:
            stat = decreased_stat
        elif decreased == "special-defense" and i == 6:
            stat = decreased_stat
        elif decreased == "speed" and i == 8:
            stat = decreased_stat
        elif increased == "attack" and i == 0:
            stat = increased_stat
        elif increased == "defense" and i == 2:
            stat = increased_stat
        elif increased == "special-attack" and i == 4:
            stat = increased_stat
        elif increased == "special-defense" and i == 6:
            stat = increased_stat
        elif increased == "speed" and i == 8:
            stat = increased_stat
        else:
            stat = normal_stat
        stats.append(stat)

    description += f"\n**Nature:** {nature}"
    description += f"\n**HP:** {hp} - IV: {hp_iv}/31"
    description += f"\n**Attack:** {stats[0]} - IV: {atk_iv}/31"
    description += f"\n**Defense:** {stats[1]} - IV: {def_iv}/31"
    description += f"\n**Sp. Atk:** {stats[2]} - IV: {spatk_iv}/31"
    description += f"\n**Sp. Def:** {stats[3]} - IV: {spdef_iv}/31"
    description += f"\n**Speed:** {stats[4]} - IV: {speed_iv}/31"

    return description, title, image

def check_evolution(poke_id, user_id, name):
    with open("pokemon.json") as f:
        data = json.load(f)

    url =  f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}/"
    r = requests.get(url)
    response_dict = r.json()

    evolution_chain = response_dict["evolution_chain"]["url"]
    r = requests.get(evolution_chain)
    response_dict = r.json()

    if name.lower() == response_dict["chain"]["species"]["name"]:
        first_evolution = True
        min_level = response_dict["chain"]["evolves_to"][0]["evolution_details"][0]["min_level"]
        trigger = response_dict["chain"]["evolves_to"][0]["evolution_details"][0]["trigger"]["name"]
    elif name.lower() == response_dict["chain"]["evolves_to"][0]["species"]["name"]:
        first_evolution = False
        second_evolution = True
        min_level = response_dict["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0]["min_level"]
        trigger = response_dict["chain"]["evolves_to"][0]["evolves_to"][0]["evolution_details"][0]["trigger"]["name"]
    else:
        min_level = 101
        trigger = "Hakuna Matata"
        print("c")

    for pokemon in data["users"][user_id]:
        if pokemon["name"] == name and pokemon["lvl"] >= min_level and trigger == "level-up":
            if first_evolution:
                name = response_dict["chain"]["evolves_to"][0]["species"]["name"]
                pokemon["name"] = name.title()
                with open("pokemon.json", "w") as file:
                    json.dump(data, file, indent=4)
                return True, name.title()
            elif second_evolution:
                name = response_dict["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
                pokemon["name"] = name.title()
                with open("pokemon.json", "w") as f:
                    json.dump(data, f, indent=4)
                return True, name.title()


    return False, "name"




def check_type(poke_id, name, user_id):
    with open("pokemon.json") as f:
        data = json.load(f)

    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}/"
    r = requests.get(url)
    response_dict = r.json()

    if len(response_dict["types"]) == 1:
        type1 = response_dict["types"][0]["type"]["name"]
    else:
        type1 = response_dict["types"][0]["type"]["name"]
        type2 = response_dict["types"][1]["type"]["name"]

    for pokemon in data["users"][user_id]:
        if pokemon["name"] == name:
            pokemon["type1"] = type1
            if "type2" in locals():
                pokemon["type2"] = type2
    
    with open("pokemon.json", "w") as f:
        json.dump(data, f, indent=4)


def return_id(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}/"
    r = requests.get(url)
    response_dict = r.json()
    poke_id = response_dict["id"]
    
    return poke_id