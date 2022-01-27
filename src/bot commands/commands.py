from pickle import NONE
from types import ModuleType
import discord
import random
from discord.ext import commands
from datetime import datetime

bot = commands.Bot(command_prefix = "!", help_command=None)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!") 

@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)

    if num == 1:
        await ctx.send("Heads!")
    if num == 2:
        await ctx.send("Tails!")

@bot.command()
async def rps(ctx, hand):
    hands =["✌️","✋","👊"]
    bothand = random.choice(hands)
    await ctx.send(bothand)
    if hands == bothand:
        await ctx.send("DRAW!")
    elif hand == "✌️":
        if bothand == "👊":
            await ctx.send("I won!")
        if bothand == "✋":
            await ctx.send("You won!")
    elif hand == "✋":
        if bothand == "👊":
            await ctx.send("You won!")
        if bothand == "✌️":
            await ctx.send("I won!")
    elif hand == "👊":
        if bothand == "✋":
            await ctx.send("I won!")
        if bothand == "✌️":
            await ctx.send("You won!")


@bot.command(aliases = ["about"])
async def help(ctx):
    MyEmbed = discord.Embed(title = "Commands", description = "Commands to use for Kebab Bot", color = discord.Colour.dark_magenta())
    MyEmbed.set_thumbnail(url = "https://i.ytimg.com/vi/HfFx5UvzSxc/maxresdefault.jpg")
    MyEmbed.add_field(name = "!ping", value = "Says pong to you!", inline=False)
    MyEmbed.add_field(name = "!coinflip", value = "Play coinflip!", inline=False)
    MyEmbed.add_field(name = "!rps", value = "Play rock scissors paper!", inline=False)
    await ctx.send(embed = MyEmbed)


@bot.group()
async def edit(ctx):
    pass

@edit.command()
async def servername(ctx,*, input):
    await ctx.guild.edit(name = input)

@edit.command()
async def createtextchannel(ctx,*, input):
    await ctx.guild.create_text_channel(name = input)

@edit.command()
async def createvoicechannel(ctx,*, input):
    await ctx.guild.create_voice_channel(name = input)

@edit.command()
async def createrole(ctx,*, input):
    await ctx.guild.create_role(name = input)

@bot.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await ctx.guild.kick(member, reason = reason)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await ctx.guild.ban(member, reason = reason)

@bot.command()
async def unban(ctx,*,input):
    name, discriminator = input.split("#")
    banned_members = await ctx.guild.bans()
    for bannedmember in banned_members:
        username = bannedmember.user.name
        disc = bannedmember.user.discriminator
        if name == username and discriminator == disc:
            await ctx.guild.unban(bannedmember.user)


@bot.command()
async def purge(ctx, amount, day = None, month : int = None, year : int = datetime.now().year):
    if amount == "/":
        if day == None or month == None:
            return
        else:
            await ctx.channel.purge(after = datetime(year, month, day))
    else:
        await ctx.channel.purge(limit = int(amount)+1)


    

bot.run("TOKEN")