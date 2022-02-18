import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix = "!", help_command=None) # command prefix (it can be changed to any symbol)
#bot is client!


@bot.event
async def on_ready():
    print("\n0=0=0=0=0=0=0=0=0=0")
    print("Ready to launch!")
    print("0=0=0=0=0=0=0=0=0=0\n")

@bot.command()
async def reload(ctx):
    bot.reload_extension("commands_cog")

bot.load_extension("commands_cog")




bot.run("TOKEN")
# #replace TOKEN with token id of bot
