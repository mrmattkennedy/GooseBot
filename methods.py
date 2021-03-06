import sys
import discord
import random
import constants
import os.path

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
        house_contents = get_household_items()
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
        lake_contents = [line.rstrip().split(constants.data_delimiter) for line in list(f)]
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
        return message_to_write

def add_command(message):
    #Must be only 1 delimiter
    if message.count(constants.add_message_delimiter) != 1:
        raise Exception("The message must have only one " + '"' + constants.add_message_delimiter + '"' + " in it")
    #Need space after token
    if message[len(constants.add_token)] != " ":
        raise Exception("The message needs a space after " + constants.add_token)

    #save the command & output of the message, and strip the whitespace
    key, output = [item.strip() for item in message[len(constants.add_token)+1:].split(constants.add_message_delimiter)]

    if not os.path.isfile(constants.user_commands_path):
        open(constants.user_commands_path, "w").close()
        
    with open(constants.user_commands_path, "r+") as f:
        current_contents = [line.rstrip().split(constants.data_delimiter) for line in list(f)]
        if any(key in keys[0] for keys in current_contents):
            raise Exception("The command already exists. Use a different key")
        
        f.write(key + constants.data_delimiter + output + "\n")

def remove_command(message):
    #Must be 0 delimiters
    if message.count(constants.add_message_delimiter) != 0:
        raise Exception("The message must have no " + '"' + constants.add_message_delimiter + '"' + " in it")
    #Need space after token
    if message[len(constants.remove_token)] != " ":
        raise Exception("The message needs a space after " + constants.remove_token)

    key = message[len(constants.remove_token)+1:].strip()
    print(key)
    #if file doesn't exist, there are no commands yet
    if not os.path.isfile(constants.user_commands_path):
        raise Exception("The command you tried to steal (remove) does not exist")

    with open(constants.user_commands_path, "r+") as f:
        current_contents = [line.rstrip().split(constants.data_delimiter) for line in list(f)]
        if any(key in commands[0] for commands in current_contents):
            index = [i for i, lst in enumerate(current_contents) if key in lst][0]
            del current_contents[index]

            f.seek(0)
            for command in current_contents:
                f.write(command[0] + constants.data_delimiter + command[1] + "\n")
            f.truncate()
        else:
            raise Exception("The command you tried to steal (remove) does not exist")

def check_channel_and_user(token, message):
    #get channel
    message_channel = message.channel
    if isinstance(message_channel, discord.channel.DMChannel):
        raise Exception("The goose is powerful, but not powerful enough to steal messages in a DM channel, sorry")

    #get server
    guild_to_check = message.guild

    #Need to get a list of members, see if they match
    if message.content[len(token)] != " ":
        raise Exception("Format: " + token + " [name]")

    #get all members that match the description from the user
    name = message.content[len(token)+1:].strip()
    matching_names = []
    for member in guild_to_check.members:
        if name == member.display_name:
            matching_names.append(member)

    #if not exactly 1 member like that, there was a problem
    if len(matching_names) == 0:
        raise Exception("The goose couldn't find anyone with the name " + '"' + name + '"')
    elif len(matching_names) > 1:
        raise Exception("The goose found more than one person with that name")

    return matching_names[0]
                
def get_user_commands():
    if not os.path.isfile(constants.user_commands_path):
        open(constants.user_commands_path, "w").close()
        
    with open(constants.user_commands_path, "r") as f:
        return [line.rstrip().split(constants.data_delimiter) for line in list(f)]
