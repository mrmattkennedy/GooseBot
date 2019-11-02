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
        return random.randrange(constants.random_messages_minimum, constants.random_messages_maximum)

def get_household_items():
    try:
        return list(open(constants.items_path, "r"))
    except:
        #File doesn't exist
        print("Error: no household items file found")
        sys.exit(1)

#Need to work on commas in items
def add_to_lake(item):
    with open(constants.lake_contents_path, "r+") as f:
        current_contents = [line.rstrip().split(constants.data_delimiter) for line in list(f)]
        
        if any(item in item_logged for item_logged in current_contents):
            index = [i for i, lst in enumerate(current_contents) if item in lst][0]
            current_contents[index][1] = str(int(current_contents[index][1]) + 1)
        elif len(current_contents) == 0:
            temp = [item.rstrip(), 1]
            current_contents.insert(0, temp)
        else:
            temp = [item.rstrip(), 1]
            current_contents.append(temp)

        print(current_contents)
        f.seek(0)
        for item_content in current_contents:
            f.write(item_content[0] + constants.data_delimiter + str(item_content[1]) + "\n")
        f.truncate()
        
#Set up variables
TOKEN = 'NjM5ODExMDg2MzQ1OTYxNDcz.Xb2Trw.FNIq9JJcxhybI7I5Nc-EVB9NX4M'
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
        stolen_item = item_list[random_index].rstrip()
        first_letter = stolen_item[:1]
        article = "a "

        if first_letter == 'a' or first_letter == 'e' or first_letter == 'i' or first_letter == 'o' or first_letter == 'u':
            article = "an "
        
        await message.channel.send("This dang goose just stole " + article + stolen_item + " and put it in the lake")
        add_to_lake(stolen_item)
        return

    #message stolen
    if rand_messages_to_delete <= 0:
        await message.delete()
        await message.channel.send(constants.loud_honk_message + " " + constants.loud_honk_message)
        await message.channel.send(constants.message_stolen)
        await message.channel.send(constants.loud_honk_message + " " + constants.loud_honk_message)
        rand_messages_to_delete = random.randrange(constants.random_messages_minimum, constants.random_messages_maximum)
        return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
