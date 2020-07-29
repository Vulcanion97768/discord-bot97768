import discord
from random import choice, randint
from pokemon_dictionary import pokemon_dict


class WildPokemon:
    def __init__(self):
        self.num_list = [x for x in range(1, 722)]
        self.random_num = randint(1, 721 )
        self.natures = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold",
        "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", 
        "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", 
        "Sassy", "Careful", "Quirky"]

    def make_pokemon(self):
        self.image = pokemon_dict[self.random_num]["image"]
        self.pokemon = pokemon_dict[self.random_num]["name"]
        self.type1 = pokemon_dict[self.random_num]["type1"]
        if "type2" in pokemon_dict[self.random_num]:
            self.type2 = pokemon_dict[self.random_num]["type2"]
        self.hp_iv = choice([x for x in range(0, 31)])
        self.atk_iv = choice([x for x in range(0, 31)])
        self.def_iv = choice([x for x in range(0, 31)])
        self.speed_iv = choice([x for x in range(0, 31)])
        self.spatk_iv = choice([x for x in range(0, 31)])
        self.spdef_iv = choice([x for x in range(0, 31)])
        self.nature = choice(self.natures)
        self.lvl = randint(1, 35)
        
    def make_embedded_pokemon(self):
        self.embed = discord.Embed(
            title="A wild pokemon has appeared!", 
            description="Guess the pokemon and type $catch <pokemon> to catch it", 
            color=0x229b30
        )
        self.embed.set_image(url=self.image)

    def reroll_pokemon(self):
        self.random_num = randint(1, 721)
        self.nature = choice(self.natures)

