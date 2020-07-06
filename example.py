import discord
from discord.ext import commands
from discord import VoiceClient

token = "NzE2ODU0MzU2ODg0MDYyMjc5.Xu8S8Q.gjM7S79ZDLmoWaVY75rgtJjrThE"
client_id = 716854356884062279
yisus = 439656238897430529
arlan = 485988534784622593
victor = 434856194952396800
luis = 395608543744753674
lore = 328645836072288256
angel = 409941082806157312
server_id = 682759984932847715
voice_channel_id = 6827599854695874734

client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    """Prints the name of the bot once it is ready"""
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    """When someone sends a message, performs a series of actions 
    dending of various conditions"""
    # Makes sure we get the number of users
    id = client.get_guild(server_id)

    # So the bot cannot respond to itself
    if message.author == client.user:
        return

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
    elif message.author.id == luis:
        if message.content.startswith("!"):
            pass
        else:
            await message.channel.send("Chinga tu cola Luis")
    elif message.author.id == victor:
        if message.content.startswith("!"):
            pass
        else:
            await message.channel.send("Chinga tu cola victor")

    elif message.content == "#users":
        await message.channel.send(f"# of Members: {id.member_count}")

    # Makes sure that the command decorator is run
    await client.process_commands(message)


# Simple test decorator used to check if commands work
@client.command()
async def test(ctx):
    print("Hello world")


# Way to get the number of users in a server
@client.command()
async def users(ctx):
    id_1 = client.get_guild(server_id)
    await ctx.send(f"# of members: {id_1.member_count}")


client.run(token)
