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
item_list = methods.get_household_items()
lake_contents = []
user_commands = methods.get_user_commands()

@client.event
async def on_message(message):
    #prevent bot from replying to itself
    if message.author == client.user:
        return

    #all other messages are legit, so decrement
    global item_list
    global lake_contents
    global user_commands

    if not message.content.startswith("!") and isinstance(message.channel, discord.channel.DMChannel):
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
        if message.content == constants.small_honk_token:
            await message.channel.send(constants.small_honk_message)
            return
        else:
            try:
                user = methods.check_channel_and_user(constants.small_honk_token, message)
                await message.channel.send(constants.small_honk_message + " " + user.mention)
                if user.dm_channel == None:
                    await user.create_dm()

                await user.dm_channel.send(message.author.display_name + " just told me to quietly honk at you, are you just gonna take that?")
                return
            except Exception as error:
                await message.channel.send(str(error))
                return
                
    #HONK
    if message.content.startswith(constants.loud_honk_token):
        if message.content == constants.loud_honk_token:
            await message.channel.send(constants.loud_honk_message)
            return
        else:
            try:
                user = methods.check_channel_and_user(constants.loud_honk_token, message)
                await message.channel.send(constants.loud_honk_message + " " + constants.loud_honk_message + " " + user.mention, tts=True)
                if user.dm_channel == None:
                    await user.create_dm()

                await user.dm_channel.send(message.author.display_name + " just told me to loudly honk at you, are you just gonna take that?")
                return
            except Exception as error:
                await message.channel.send(str(error))
                return

    #steal, make it so this will steal their last non-command message
    if message.content.startswith(constants.steal_message_token):
        if message.content.strip() == constants.steal_message_token:
            random_index = random.randrange(len(item_list))
            stolen_item = item_list[random_index].rstrip()
            first_letter = stolen_item[:1]
            article = "a "

            if first_letter == 'a' or first_letter == 'e' or first_letter == 'i' or first_letter == 'o' or first_letter == 'u':
                article = "an "
            
            await message.channel.send("This dang goose just stole " + article + stolen_item + " and put it in the lake")
            methods.add_to_lake(stolen_item)
        else:
            try:
                name = methods.check_channel_and_user(constants.steal_message_token, message).display_name
                
                #get last 100 messages from that channel
                async for previous_message in message.channel.history(limit=100):
                    if previous_message.author.display_name == name:
                        #Delete message, send 2 loud honks, then send random image (2 choices)
                        await previous_message.delete()
                        await message.channel.send(constants.loud_honk_message + " " + constants.loud_honk_message)
                        await message.channel.send(constants.other_message_stolen + '"' + previous_message.content + '" from **' + previous_message.author.display_name + '**')
                        image = ((lambda: constants.stolen_image_one_path, lambda: constants.stolen_image_two_path)[random.randint(1, 2) == 1]())
                        await message.channel.send(file=discord.File(image))
                        
                        methods.steal_message(previous_message.author.display_name, previous_message.content)
                        break
                return
            except Exception as error:
                await message.channel.send(str(error))
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
    if len(message.content) < 1:
        return
    if any(message.content[1:] in command[0] for command in user_commands):
        index = [i for i, lst in enumerate(user_commands) if message.content[1:] in lst][0]
        await message.channel.send(user_commands[index][1])
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
