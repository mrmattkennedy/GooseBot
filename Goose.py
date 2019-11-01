# Work with Python 3.6
import sys
import discord
import random
import constants

def get_messages_until_delete():

    try:
        f = open(constants.counter_file_path, "r")
        return int(f.read())
    except:
        return random.randrange(7, 13, 1)

def get_household_items():
    try:
        return list(open(constants.items_path, "r"))
    except:
        #File doesn't exist
        print("Error: no household items file found")
        sys.exit(1)
"""
Set up varaibles. Need:
token,
client,
number of messages until delete,
list of items,
current lake contents
"""

TOKEN = 'NjM5ODExMDg2MzQ1OTYxNDcz.XbxmVw.c0HYtD2KFqypeiEkrJw-LXAX0ag'
client = discord.Client()
rand_messages_to_delete = get_messages_until_delete()
item_list = get_household_items()
print(type(item_list))

@client.event
async def on_message(message):
    #prevent bot from replying to itself
    if message.author == client.user:
        return
    
    #all other messages are legit, so decrement
    global rand_messages_to_delete
    global item_list
    
    rand_messages_to_delete-=1
    print(rand_messages_to_delete)
    
    #honk
    if message.content.startswith(constants.small_honk_token):
        await message.channel.send(constants.small_honk_message)
        return

    #HONK
    if message.content.startswith(constants.loud_honk_token):
        await message.channel.send(constants.loud_honk_message, tts = True)
        return

    #steal
    if message.content.startswith(constants.steal_message_token):
        random_index = random.randrange(len(item_list))
        await message.channel.send("This dang goose just stole a " + item_list[random_index].rstrip() + " and put it in the lake")
        return

    #message stolen
    if rand_messages_to_delete <= 0:
        await message.delete()
        await message.channel.send(constants.loud_honk_message + " " + constants.loud_honk_message)
        await message.channel.send(constants.message_stolen)
        await message.channel.send(constants.loud_honk_message + " " + constants.loud_honk_message)
        rand_messages_to_delete = random.randrange(7, 13, 1)
        return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
