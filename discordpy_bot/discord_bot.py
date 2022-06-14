# Kudos to Anonymoos, hope it will help you :)

#!/usr/bin/python3

# First of all...
# Here's the discord.py documentation 
# https://discordpy.readthedocs.io/en/stable/api.html
# It's not very user-friendly but having it on the side will help you a lot

# Import the needed libraries
import discord
from discord.ext import commands
from discord_components import ComponentsBot

# Set the bot token here
TOKEN 		= ""

# We can let our bot be accessible in every channels,
# or we can filter the channel in which commands are allowed.
# In this example I want to filter so users can interract with my bot only in the #demo channel
channel_cmd = ""

# Instanciate the bot object and set the command delimiter.
# You can use any other character if you want
bot			= ComponentsBot("!")

# This function will be called when the bot is started
@bot.event
async def on_ready():
	global guild
	guild = bot.guilds[0]
	print("Bot started")


###############################
# Help command handler
###############################
# We have to do a small trick to delete the default 'help' command handler before creating our own one
bot.remove_command("help")

# Then we create our own help handler :)
@bot.command(name="help",aliases=['h'])
async def help_command(ctx):
	# Here is the channel filtering, if you remove this line (and re-indent the following code)
	# then the bot will answer to users in every channels.
	# You can filter on multiples channels with a 'if' with multiple statements
	if str(ctx.message.channel.id) == str(channel_cmd):
		# Here we simply create the variable containing the help menu text
		data = """
This is a simple help menu :)
\n
**🦖 !echo (text) :**\n`The bot will show the message you sent.`
\n
**🪙 !help :**\n`This beautiful help menu.`
\n
		"""

		# To send messages we can:
		# 1. Send a new message in the channel with: ctx.message.channel.send
		# OR
		# 2. Reply to the user's message with: ctx.message.reply 
		await ctx.message.channel.send(data)

###############################
# Echo command handler
###############################
# This handler is not created by default so we don't have to do the little trick
# we did earlier.
@bot.command(name="echo",aliases=['e'])
async def echo(ctx):
	# Again, checking if the message is sent in an allowed channel
	if str(ctx.message.channel.id) == str(channel_cmd):
		# Here I create the response content.
		#
		# ctx.message is an object representation of the message the user sent
		# It comes with multiple usefull attributes like author or content for example.
		message_content = "🦖🪙 %s sent: `%s`" % (ctx.message.author, ctx.message.content)
		await ctx.message.reply(message_content)

# After declaring everything, we can start our bot !
bot.run(TOKEN)