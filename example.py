import discord
from discord.ext import commands
import requests
from id_info import ids
from pokemon_dictionary import dict
from id_info import ids
from message_counter import MessageCounter


client = commands.Bot(command_prefix='$')
message_counter = MessageCounter()

@client.event
async def on_ready():
    """Prints the name of the bot once it is ready"""
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    """When someone sends a message, performs a series of actions 
    dending of various conditions"""
    # So the bot cannot respond to itself
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

    if message_counter.message_count == 10:
        message_counter.reset_count()
        await message.channel.send("puta")
        

    # Makes sure that the command decorator is run
    await client.process_commands(message)


# Way to get the number of users in a server
@client.command()
async def users(ctx):
    id_1 = client.get_guild(ids["server_id"])
    await ctx.send(f"# of members: {id_1.member_count}")

# Sends the image of any pokemon along with its name    
@client.command()
async def image(ctx, arg):
    embed = discord.Embed(
        title = str(dict[int(arg)]["name"])
    )
    embed.set_image(url=dict[int(arg)]["image"])
    await ctx.send(embed=embed)

client.run(ids["token"])
