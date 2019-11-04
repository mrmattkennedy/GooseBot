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

def add_to_lake(item):
    #Open the file for reading and writing
    with open(constants.lake_contents_path, "r+") as f:
        #Get each line of the file into a list of lists, splitting each line with the delimiter
        current_contents = [line.rstrip().split(constants.data_delimiter) for line in list(f)]
        
        #If item is part of the household list, incremenet
        house_contents = list(item_list)
        if any(item in line for line in house_contents):
            
            #If the item exists, it will return true here
            if any(item in item_logged for item_logged in current_contents):
                #Set the index to the first instance of the item in current contents
                index = [i for i, lst in enumerate(current_contents) if item in lst][0]
                #Incremement count by 1
                current_contents[index][1] = str(int(current_contents[index][1]) + 1)
            else:
                temp = [item.rstrip(), 1]
                current_contents.insert(0, temp)

            #overwrite what is there so start from beginning
            f.seek(0)
            for item_content in current_contents:
                if (len(item_content) == 2):
                    f.write(item_content[0] + constants.data_delimiter + str(item_content[1]) + "\n")
                else:
                    f.write(item_content[0] + "\n")
            f.truncate()
            
def steal_message(author, message):
    with open(constants.lake_contents_path, "r+") as f:
        #Get each line of the file into a list of lists, splitting each line with the delimiter
        current_contents = [line.rstrip().split(constants.data_delimiter) for line in list(f)]

        #see if delimiter exists. If not, add it
        if not any(constants.stolen_message_delimiter in item for item in current_contents):
            current_contents.append([constants.stolen_message_delimiter])

        #** to bold username
        current_contents.append(["**" + author + "**" + " tried to send: " + '"' + message + '"'])
        #overwrite what is there so start from beginning
        f.seek(0)
        for item_content in current_contents:
            if (len(item_content) == 2):
                f.write(item_content[0] + constants.data_delimiter + str(item_content[1]) + "\n")
            else:
                f.write(item_content[0] + "\n")
        f.truncate()
    
def read_lake_contents():
    with open(constants.lake_contents_path, "r") as f:
        #Get each line of the file into a list of lists, splitting each line with the delimiter
        return [line.rstrip().split(constants.data_delimiter) for line in list(f)]


        
#Set up variables
TOKEN = 'NjM5ODExMDg2MzQ1OTYxNDcz.XcAwZQ.RRcXOmf_Q_ZuyF1_u5GWW444yE8'
client = discord.Client()
rand_messages_to_delete = get_messages_until_delete()
item_list = get_household_items()
lake_contents = []

@client.event
async def on_message(message):
    #prevent bot from replying to itself
    if message.author == client.user:
        return
    
    #all other messages are legit, so decrement
    global rand_messages_to_delete
    global item_list
    global lake_contents

    #if not a DM, then decrement stolen message counter
    if not isinstance(message.channel, discord.channel.DMChannel):
        rand_messages_to_delete-=1
        print(rand_messages_to_delete)
    elif not message.content.startswith("!"):
        random_insult = random.randint(0, len(constants.dm_insults) - 1)
        await message.channel.send(constants.dm_insults[random_insult])

    #help
    if message.content.startswith(constants.help_token):
        await message.channel.send(constants.help_message)
        return
    
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

    #lake
    if message.content.startswith(constants.lake_contents_token):
        lake_contents = read_lake_contents()
        message_to_write = "The goose has stolen:\n"
        for item in lake_contents:
            if len(item) == 2:
                first_letter = item[0][:1]
                article = "a "

                #ternary operator: if more than 1 occurance of stealing, use times, else, use time
                times_plural_word = ((lambda: " time", lambda: " times")[int(item[1]) > 1]())
                if first_letter == 'a' or first_letter == 'e' or first_letter == 'i' or first_letter == 'o' or first_letter == 'u':
                    article = "an "
                message_to_write += article + item[0] + " " + item[1] + times_plural_word + "\n"
            else:
                if item[0] == constants.stolen_message_delimiter:
                    message_to_write += "\n" + "The goose has also stolen the following messages:\n"
                else:
                    message_to_write += item[0] + "\n"
        await message.channel.send(message_to_write)
        return

    #message stolen
    if rand_messages_to_delete <= 0:

        #Delete message, send 2 loud honks, then send random image (2 choices)
        await message.delete()
        await message.channel.send(constants.loud_honk_message + " " + constants.loud_honk_message)
        await message.channel.send(constants.message_stolen)
        image = ((lambda: constants.stolen_image_one_path, lambda: constants.stolen_image_two_path)[random.randint(1, 2) == 1]())
        await message.channel.send(file=discord.File(image))
        
        rand_messages_to_delete = random.randrange(constants.random_messages_minimum, constants.random_messages_maximum)
        steal_message(message.author.display_name, message.content)
        return

@client.event
async def on_ready():
    print('Goose bot ready')
    print('------')
    game = discord.Game(name="PM me !help")
    #activity = discord.Activity(name="HONK", type=4) #doesn't work yet for custom statuses
    await client.change_presence(activity=game)

try:
    client.run(TOKEN)
except discord.errors.LoginFailure as token_error:
    if str(token_error) == constants.token_error_message: #if specifically bad token error
        print(str(token_error))
    else:
        raise
except:
    print(sys.exc_info()[0])
