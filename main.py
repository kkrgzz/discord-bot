import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix = "!", help_command=None) # command prefix (it can be changed to any symbol)
#bot is client!


@bot.command()
async def reload(ctx):
    for file in os.listdir("/src/bot_commands/"):
        bot.reload_extension("bot_commands.commands_cog")

for file in os.listdir("/src/bot_commands/"):
    bot.load_extension("bot_commands.commands_cog")




bot.run("TOKEN")
# #replace TOKEN with token id of bot
