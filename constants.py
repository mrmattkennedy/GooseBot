counter_file_path = "messages_until_delete.dat"
items_path = "data/household_items.dat"
lake_contents_path = "data/current_lake_contents.dat"
user_commands_path = "data/user_commands.dat"

data_delimiter = "..."
stolen_message_delimiter = "==="
add_message_delimiter = "..."

stolen_image_one_path = "pictures/stolen-1.png"
stolen_image_two_path = "pictures/stolen-2.jpg"

token_error_message = "Bad token has been passed."

random_messages_minimum = 20
random_messages_maximum = 30

small_honk_token = "!honk"
small_honk_message = "honk"
loud_honk_token = "!HONK"
loud_honk_message = "HONK"
steal_message_token = "!steal"
lake_contents_token = "!lake"
help_token = "!help"
add_token = "!add"
add_confirmed = "Command successfully stolen (saved)"
add_failed = "Failed to steal (save) command"
add_usage = "Usage: !add [key]...[message], Example: !add sing...the goose can only honk"
remove_token = "!remove"
remove_confirmed = "Command successfully stolen (removed)"
remove_failed = "Failed to steal (remove) command)"
remove_usage = "Usage: !remove [key]. Example: !remove sing"

help_message = """HONK HONK\n
!honk [optional: name]:\tsmol honk, or honk at someone
!HONK [optional: name]:\tL O U D honk, or do it at someone
!steal [optional: name]:\tThe goose will steal something. If you add someone's name, it will steal their last message in that channel (checks last 100 messages in the channel)
!lake:\tsee what the goose has stolen so far
!add [key]...[message]\tAdds a custom command, where if you type !key, the bot will send the message
!remove [key]\tRemoves a custom command made by the user\n
"""

message_stolen = "The goose has stolen your message! Better check the lake..."
other_message_stolen = "Goose has successfuly stolen "

dm_insults = ["I will steal your rake", "You are a stinky boy", "I am silver-global-grandmaster-elite in CS:GO"]
