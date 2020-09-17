import discord
from discord.ext import commands
import csv
import json
import requests
# import pymongo
from random import randint, choice
from math import ceil, floor
from id_info import ids
from pokemon_dictionary import pokemon_dict
from message_counter import MessageCounter
from wild_pokemon import WildPokemon
from functions import add_experience, check_experience, return_info, check_type, return_id


# mongo_client = pymongo.MongoClient("mongodb+srv://discord-bot:mensomemo123@cluster0.6t6qh.mongodb.net/pokemon?retryWrites=true&w=majority")
# db = mongo_client.test
client = commands.Bot(command_prefix='$')
message_counter = MessageCounter()
wild_pokemon = WildPokemon()
professor_oak = "https://giantbomb1.cbsistatic.com/uploads/square_medium/8/84561/1465705-professor_oak_anime.png"


@client.event
async def on_ready():
    """Prints the name of the bot once it is ready"""
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    """When someone sends a message, performs a series of actions 
    dending of various conditions"""
    # So the bot cannot respond to itself
    user_id = str(message.author.id)
    if message.author == client.user:
        return

    message_counter.add_to_count()

    # Message.content.find return a -1 if message isn't found in the content
    if message.content.find("hello") != -1:
        await message.channel.send("Que rollo zorra!!!")

    # Check for the word popo in any part of the message
    if "popo" in message.content.lower():
        await message.channel.send("popo")

    # Check for the message to start with the word caca
    elif message.content.startswith("caca"):
        await message.channel.send(file=discord.File("caca.png"))

    # Checks if the id of whoever sent the message corresponds to a certain user
    elif message.author.id == ids["luis"]:
        if message.content.startswith("!"):
            pass
        else:
            await message.channel.send("Chinga tu cola Luis")
    elif message.author.id == ids["victor"]:
        if message.content.startswith("!"):
            pass
        else:
            await message.channel.send("Chinga tu cola victor")

    # Makes sure that once three messages are sent, a new pokemon appears
    if message_counter.message_count == 10:
        wild_pokemon.reroll_pokemon()
        wild_pokemon.make_pokemon()
        wild_pokemon.make_embedded_pokemon()
        message_counter.reset_count()
        message_counter.pokemon_available = True
        await message.channel.send(embed=wild_pokemon.embed)

    random_stone = ["thunder-stone", "ice-stone", "moon-stone",
                    "fire-stone", "leaf-stone", "sun-stone", "water-stone", 
                    "shiny-stone", "dusk-stone", "dawn-stone"]
    if message_counter.inventory_count == 55:
        with open("inventory.json") as f:
            data = json.load(f)
        user_id = str(message.author.id)
        if user_id in data:
            stone = choice(random_stone)
            data[user_id].append(stone)
        else:
            stone = choice(random_stone)
            data[user_id] = [stone]
        with open("inventory.json", "w") as f:
            json.dump(data, f, indent=4)
        send_message = True
        message_counter.reset_inventory_count()

    try:
        if send_message:
            await message.channel.send(f"Congratulations, \
                                        you just received a {stone}")
    except UnboundLocalError:
        pass

    add_experience(user_id)
    evol_active, evolution, active, name, lvl = check_experience(user_id)
    author = str(message.author)
    author1 = author.split("#")
    if evol_active:
        await message.channel.send(f"Congratulations @{author1[0]}, your {name} evolved into a {evolution}")
    elif active:
        await message.channel.send(f"Congratulations @{author1[0]}, your {name} is now level {lvl}")

    # Makes sure that the command decorator is run
    await client.process_commands(message)


@client.command()
async def users(ctx):
    # Way to get the number of users in a server
    id_1 = client.get_guild(ids["server_id"])
    await ctx.send(f"# of members: {id_1.member_count}")


@client.command()
async def image(ctx, arg):
    # Sends the image of any pokemon along with its name
    embed = discord.Embed(
        title=str(pokemon_dict[int(arg)]["name"])
    )
    embed.set_image(url=pokemon_dict[int(arg)]["image"])
    print(pokemon_dict[int(arg)]["name"])
    await ctx.send(embed=embed)


@client.command()
async def catch(ctx, arg):
    # Catches pokemons when they appear and registers them in a json file
    pokemon = wild_pokemon.pokemon.lower()
    # If the user guesses the pokemon name, the pokemon 
    # is captured and written in a json file
    if arg == pokemon and message_counter.pokemon_available:
        message_counter.pokemon_available = False
        with open("pokemon.json") as file:
            data = json.load(file)
        user_id = str(ctx.author.id)
        default_dict = {}
        if user_id in data["users"]:
            data["users"][user_id].append(default_dict)
            data["users"][user_id][-1]["name"] = wild_pokemon.pokemon
            data["users"][user_id][-1]["type1"] = wild_pokemon.type1
            if "type2" in pokemon_dict[wild_pokemon.random_num]:
                data["users"][user_id][-1]["type2"] = wild_pokemon.type2
            data["users"][user_id][-1]["lvl"] = wild_pokemon.lvl
            data["users"][user_id][-1]["exp"] = int(
                (4 * wild_pokemon.lvl**3) / 5)
            data["users"][user_id][-1]["selected"] = False
            data["users"][user_id][-1]["hp_iv"] = wild_pokemon.hp_iv
            data["users"][user_id][-1]["atk_iv"] = wild_pokemon.atk_iv
            data["users"][user_id][-1]["def_iv"] = wild_pokemon.def_iv
            data["users"][user_id][-1]["speed_iv"] = wild_pokemon.speed_iv
            data["users"][user_id][-1]["spatk_iv"] = wild_pokemon.spatk_iv
            data["users"][user_id][-1]["spdef_iv"] = wild_pokemon.spdef_iv
            data["users"][user_id][-1]["nature"] = wild_pokemon.nature
            data["users"][user_id][-1]["happiness"] = wild_pokemon.happiness
            with open("pokemon.json", "w") as file:
                json.dump(data, file, indent=4)
            x = str(ctx.author)
            y = x.split("#")
            author = y[0]
            await ctx.send(f"Congratulations @{author}, you just caught a {wild_pokemon.pokemon}")
        else:
            await ctx.send("You need to pick a starter pokemon before being able to use this command")
    elif arg != wild_pokemon.pokemon.lower():
        await ctx.send("That's not the correct pokemon")


@client.command()
async def pokemon(ctx, *args):
    # Gives info about the pokemons the user has
    with open("pokemon.json") as file:
        data = json.load(file)
    description = "Your pokemon:"
    user_id = str(ctx.author.id)
    pokemons = []
    if user_id in data["users"]:
        lenght = len(data["users"][user_id])
        i = 1
        """
        for pokemon in data["users"][user_id]:
            pokemons[pokemon["name"]] = {}
            pokemons[pokemon["name"]]["name"] = pokemon["name"]
            pokemons[pokemon["name"]]["lvl"] = pokemon["lvl"]
            pokemons[pokemon["name"]]["index"] = i
            i += 1
        """
        for i in range(0, lenght):
            info = [data["users"][user_id][i]["name"],
                    data["users"][user_id][i]["lvl"], i+1]
            pokemons.append(info)
        pokemons.sort(key=lambda x: x[0])
        num = ceil(lenght / 20)
        nums = []
        for i in range(1, num+1):
            nums.append(str(i))
        for i in nums:
            if i in args or not args:
                start = 20 * (int(i) - 1)
                end = 20 * int(i)
                for j in range(start, end):
                    try:
                        name = pokemons[j][0]
                        lvl = pokemons[j][1]
                        index = pokemons[j][2]
                        description += f"\n**{name}** | Level: {lvl} | Number: {index}"
                        text = f"Showing {start+1}-{end} out of {lenght}"
                    except IndexError:
                        text = f"Showing {start+1}-{j} out of {lenght}"
                        break
                embed = discord.Embed(description=description)
                embed.set_footer(text=text)
                await ctx.send(embed=embed)
                break
            elif int(nums[-1]) < int(args[0]):
                await ctx.send("You don't have that many pokemon")
                break

        """
        if not args or '1' in args:
            if lenght > 20:
                for i in range(0, 20):
                    name = pokemons[i][0]
                    lvl = pokemons[i][1]
                    index = pokemons[i][2]
                    description += f"\n**{name}** | Level: {lvl} | Number: {index}"
            else:
                for i in range(0, lenght):
                    name = pokemons[i][0]
                    lvl = pokemons[i][1]
                    index = pokemons[i][2]
                    description += f"\n**{name}** | Level: {lvl} | Number: {index}"   
        elif "2" in args:
            if lenght > 40:
                for i in range(21, 41):
                    name = 4
            
        
        j = 0
        for pokemon in sorted(pokemons):
            if (not args or "1" in args) and j < 20: 
                name = pokemons[pokemon]["name"]
                lvl = pokemons[pokemon]["lvl"]
                index = pokemons[pokemon]["index"]
                description += f"\n**{name}** | Level: {lvl} | Number {index}"
                j += 1
            elif "2" in args and j < 20:
                for i in range(0, 20):
                    pass
                name = pokemons[pokemon]["name"]
                lvl = pokemons[pokemon]["lvl"]
                index = pokemons[pokemon]["index"]
                description += f"\n**{name}** | Level: {lvl} | Number {index}"
                j += 1

        for i in range(0, lenght):
            name = data["users"][user_id][i]["name"]
            lvl = data["users"][user_id][i]["lvl"]
            index = i
            description += f"\n**{name}** | Level: {lvl} | Number {index}"
        """

    """
    if "1" in args or not args:
        if lenght <= 20:
            embed.set_footer(text=f"Showing {lenght} out of {lenght} pokemon")
        elif lenght > 20:
            embed.set_footer(text=f"Showing 1-20 out of {lenght} pokemon")

    """


@client.command()
async def start(ctx, *args):
    # Sends a message with all the instructions to start the game
    if not args:
        url = "https://www.syfy.com/sites/syfy/files/styles/1200x680_hero/public/wire/legacy/2016/11/pokemon_Custom.jpg"
        embed = discord.Embed(
            title="Welcome to the wonderful world of pokemon!",
            description="Please select one starter from one of the 6 regions \
             by typing $start and the name of your starter"
        )
        embed.set_image(url=url)
        embed.set_author(name="Professor Oak", icon_url=professor_oak)
        embed.add_field(name="Generation I",
                        value="Bulbasaur | Squirtle | Charmander", inline=False)
        embed.add_field(name="Genertion II",
                        value="Chikorita | Totodile | Cyndaquil", inline=False)
        embed.add_field(name="Generation III",
                        value="Treecko | Mudkip | Torchic", inline=False)
        embed.add_field(name="Generation IV",
                        value="Turtwig | Piplup | Chimchar", inline=False)
        embed.add_field(name="Generation V",
                        value="Snivy | Oshawott | Tepig", inline=False)
        embed.add_field(name="Generation VI",
                        value="Chespin | Froakie | Fennekin", inline=False)
        await ctx.send(embed=embed)

    else:
        # If the user writes a pokemon name, 
        # the user will receive the pokemon along with variou stats
        user_id = str(ctx.author.id)
        for key, item in pokemon_dict.items():
            if item["name"].lower() in args or item["name"] in args:
                
                with open("pokemon.json") as file:
                    first_time = json.load(file)
                first_time["users"][user_id] = [{}]
                first_time["users"][user_id][0]["name"] = item["name"]
                first_time["users"][user_id][0]["type1"] = item["type1"]
                if "type2" in item:
                    first_time["users"][user_id][0]["type2"] = item["type2"]
                first_time["users"][user_id][0]["lvl"] = 1
                first_time["users"][user_id][0]["exp"] = 0
                first_time["users"][user_id][0]["selected"] = True
                first_time["users"][user_id][-1]["hp_iv"] = randint(0, 31)
                first_time["users"][user_id][-1]["atk_iv"] = randint(0, 31)
                first_time["users"][user_id][-1]["def_iv"] = randint(0, 31)
                first_time["users"][user_id][-1]["speed_iv"] = randint(0, 31)
                first_time["users"][user_id][-1]["spatk_iv"] = randint(0, 31)
                first_time["users"][user_id][-1]["spdef_iv"] = randint(0, 31)
                first_time["users"][user_id][-1]["nature"] = choice(
                    wild_pokemon.natures)
                first_time["users"][user_id][-1]["happiness"] = 50
                with open("pokemon.json", "w") as file:
                    json.dump(first_time, file, indent=4)
                """
                This inserts a pokemon at mongoDB
                db = mongo_client["Pokemon"]
                collection = db[user_id]
                pokemon = {}
                pokemon["_id"] = 1
                pokemon["name"] = item["name"]
                pokemon["type1"] = item["type1"]
                if "type2" in item:
                    pokemon["type2"] = item["type2"]
                pokemon["lvl"] = 1
                pokemon["exp"] = 0
                pokemon["selected"] = True
                pokemon["hp_iv"] = randint(0, 31)
                pokemon["atk_iv"] = randint(0, 31)
                pokemon["def_iv"] = randint(0, 31)
                pokemon["speed_iv"] = randint(0, 31)
                pokemon["spatk_iv"] = randint(0, 31)
                pokemon["spdef_iv"] = randint(0, 31)
                pokemon["nature"] = choice(wild_pokemon.natures)
                pokemon["happiness"] = 50
                collection.insert_one(pokemon)
                """
                embed = discord.Embed(
                    title="Congratulations!",
                    description="You just got your first pokemon, keep \
                        sending messages to level up your pokemon"
                )
                embed.set_author(name="Professor Oak", icon_url=professor_oak)
                embed.set_image(url=item["image"])
                await ctx.send(embed=embed)


@client.command()
async def info(ctx, *args):
    # Gives specific info about a certain pokemon
    user_id = str(ctx.author.id)
    with open("pokemon.json") as file:
        data = json.load(file)
    if args:
        description, title, image, stats = return_info(args, user_id, data)
    else:
        for pokemon in data["users"][user_id]:
            if pokemon["selected"]:
                arg = [data["users"][user_id].index(pokemon)+1]
                description, title, image, stats = return_info(
                    arg, user_id, data)

    avatar = ctx.author.avatar_url
    embed = discord.Embed(
        title=title,
        description=description
    )
    embed.set_thumbnail(url=avatar)
    embed.set_image(url=image)
    embed.set_author(name="Professor Oak", icon_url=professor_oak)
    await ctx.send(embed=embed)


@client.command()
async def select(ctx, arg):
    # Allows the user to select a pokemon so it receives experience
    user_id = str(ctx.author.id)
    with open("pokemon.json") as f:
        data = json.load(f)
    if user_id in data["users"]:
        lenght = len(data["users"][user_id])
        if lenght >= 2:
            for i in range(lenght):
                data["users"][user_id][i]["selected"] = False
            data["users"][user_id][int(arg)-1]["selected"] = True
            name = data["users"][user_id][int(arg)-1]["name"]
            with open("pokemon.json", "w") as f:
                json.dump(data, f, indent=4)
            embed = discord.Embed(
                description=f"""You just selected {name}.
                He will be receiving experience from now on.
                """
            )
            await ctx.send(embed=embed)


@client.command()
async def release(ctx, arg):
    # Allows the user to release a pokemon, deleting it from the json file
    user_id = str(ctx.author.id)
    with open("pokemon.json") as file:
        data = json.load(file)
    if user_id in data["users"]:
        index = int(arg) - 1
        if not data["users"][user_id][index]["selected"]:
            name = data["users"][user_id][index]["name"]
            data["users"][user_id].pop(index)
            with open("pokemon.json", "w") as f:
                json.dump(data, f, indent=4)
            await ctx.send(f"You just released {name}. He will\
                            never forget you :()")
        else:
            await ctx.send("Select another pokemon if you want\
                            to release this one :(")


@client.command()
async def use(ctx, arg):
    user_id = str(ctx.author.id)
    with open("pokemon.json") as file:
        data = json.load(file)
    with open("inventory.json") as f:
        inventory = json.load(f)

    if user_id in data["users"]:
        for pokemon in data["users"][user_id]:
            if pokemon["selected"]:
                name = pokemon["name"]
                url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
                r = requests.get(url)
                response_dict = r.json()

                pokemon_id = response_dict["id"]
                url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
                r = requests.get(url)
                response_dict = r.json()

                chain = response_dict["evolution_chain"]["url"]
                r = requests.get(chain)
                response_dict = r.json()

                if name.lower() == response_dict["chain"]["species"]["name"]:
                    stone = (response_dict["chain"]["evolves_to"][0]
                            ["evolution_details"][0]["item"]["name"])
                    if stone == arg and stone in inventory[user_id]:
                        previous_name = pokemon["name"]
                        name = (response_dict["chain"]["evolves_to"]
                                [0]["species"]["name"])
                        pokemon["name"] = name.title()
                        with open("pokemon.json", "w") as f:
                            json.dump(data, f, indent=4)
                        poke_id = return_id(name)
                        check_type(poke_id, name, user_id)
                        inventory[user_id].remove(stone)
                        with open("inventory.json", "w") as f:
                            json.dump(inventory, f, indent=4)
                        active = True
                    else:
                        active = False
                        
                elif name.lower() == (response_dict["chain"]["evolves_to"]
                                      [0]["species"]["name"]):
                    stone = (response_dict["chain"]["evolves_to"][0]
                             ["evolves_to"][0]["evolution_details"]
                             [0]["item"]["name"])
                    if stone == arg and stone in inventory[user_id]:
                        previous_name = pokemon["name"]
                        name = (response_dict["chain"]["evolves_to"][0]
                                ["evolves_to"][0]["species"]["name"])
                        pokemon["name"] = name.title()
                        with open("pokemon.json", "w") as f:
                            json.dump(data, f, indent=4)
                        poke_id = return_id(name)
                        check_type(poke_id, name, user_id)
                        inventory[user_id].remove(stone)
                        with open("inventory.json", "w") as f:
                            json.dump(inventory, f, indent=4)
                        active = True
                    else:
                        active = False

                else:
                    active = False
                
                if active:
                    author = str(ctx.author)
                    author1 = author.split("#")
                    await ctx.send(f"Congratulations @{author1[0]}, your {previous_name} evolved into a {name.title()}")


client.run(ids["token"])
