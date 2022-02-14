import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix = "!", help_command=None) # command prefix (it can be changed to any symbol)
#bot is client!


@bot.command()
async def reload(ctx):
    bot.reload_extension("commands_cog")

bot.load_extension("commands_cog")




bot.run("TOKEN")
# #replace TOKEN with token id of bot
