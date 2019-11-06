# Work with Python 3.6
import discord
import random
import traceback
import constants
import methods
import current_token
import sys
        
#Set up variables
client = discord.Client()
rand_messages_to_delete = methods.get_messages_until_delete()
item_list = methods.get_household_items()
lake_contents = []
user_commands = methods.get_user_commands()

@client.event
async def on_message(message):
    #prevent bot from replying to itself
    if message.author == client.user:
        return

    #all other messages are legit, so decrement
    global rand_messages_to_delete
    global item_list
    global lake_contents
    global user_commands

    #if not a DM, then decrement stolen message counter
    if not isinstance(message.channel, discord.channel.DMChannel):
        rand_messages_to_delete-=1
        print(rand_messages_to_delete)
    elif not message.content.startswith("!"):
        random_insult = random.randint(0, len(constants.dm_insults) - 1)
        await message.channel.send(constants.dm_insults[random_insult])

    #help
    if message.content.startswith(constants.help_token):
        command_string = constants.help_message
        command_string += "User created commands:\n"
        for command in user_commands:
            command_string += "!" + command[0] + "\n"
        command_string += "\nYou can PM me any of these commands, or send them in a server I'm a part of!"
        await message.channel.send(command_string) 
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
        methods.add_to_lake(stolen_item)
        return

    #lake
    if message.content.startswith(constants.lake_contents_token):        
        await message.channel.send(methods.read_lake_contents())
        return

    #add
    if message.content.startswith(constants.add_token):
        if message.content.strip() == constants.add_token:
            await message.channel.send(constants.add_usage)
            return
        try:
            methods.add_command(message.content)
            await message.channel.send(constants.add_confirmed)
            user_commands = methods.get_user_commands()
            return
        except Exception as e:
            await message.channel.send(constants.add_failed + ": " + str(e))
            #traceback.print_exc()
            return

    #remove
    if message.content.startswith(constants.remove_token):
        #just the token, print usage
        if message.content.strip() == constants.remove_token:
            await message.channel.send(constants.remove_usage)
            return
        try:
            methods.remove_command(message.content)
            await message.channel.send(constants.remove_confirmed)
            user_commands = methods.get_user_commands()
            return
        except Exception as e:
            await message.channel.send(constants.remove_failed + ": " + str(e))
            #traceback.print_exc()
            return

    #user command
    if any(message.content[1:] in command[0] for command in user_commands):
        index = [i for i, lst in enumerate(user_commands) if message.content[1:] in lst][0]
        await message.channel.send(user_commands[index][1])
        return
        
    #message stolen
    if rand_messages_to_delete <= 0 and not isinstance(message.channel, discord.channel.DMChannel):
        #Delete message, send 2 loud honks, then send random image (2 choices)
        await message.delete()
        await message.channel.send(constants.loud_honk_message + " " + constants.loud_honk_message)
        await message.channel.send(constants.message_stolen)
        image = ((lambda: constants.stolen_image_one_path, lambda: constants.stolen_image_two_path)[random.randint(1, 2) == 1]())
        await message.channel.send(file=discord.File(image))
        
        rand_messages_to_delete = random.randrange(constants.random_messages_minimum, constants.random_messages_maximum)
        methods.steal_message(message.author.display_name, message.content)
        return

@client.event
async def on_ready():
    print('Goose bot ready')
    print('------')
    game = discord.Game(name="PM me !help")
    #activity = discord.Activity(name="HONK", type=4) #doesn't work yet for custom statuses
    await client.change_presence(activity=game)

try:
    client.run(current_token.token)
except discord.errors.LoginFailure as token_error:
    if str(token_error) == constants.token_error_message: #if specifically bad token error
        print(str(token_error))
    else:
        raise
