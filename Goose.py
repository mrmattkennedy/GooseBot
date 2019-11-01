# Work with Python 3.6
import discord
import random
import constants

def get_messages_until_delete():

    try:
        f = open(constants.counter_file_path, "r")
        return int(f.read())
    except:
        return random.randrange(7, 13, 1)
    

"""Set up varaibles. Need:
token,
client,
number of messages until delete,
list of items,
list of colors,
current lake contents
"""

TOKEN = 'NjM5ODExMDg2MzQ1OTYxNDcz.XbwvWw.Zc67GJj2kD5lbbEljlqGmtXt_zI'
client = discord.Client()
rand_messages_to_delete = get_messages_until_delete()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(constants.small_honk_token):
        await message.channel.send(constants.small_honk_message)
        
    if message.content.startswith(constants.loud_honk_token):
        #await message.delete(); #how to delete
        await message.channel.send(constants.loud_honk_message, tts = True)
      

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
