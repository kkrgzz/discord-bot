"""
Bot Commands for Discord Bot
Further updates will be included soon.
"""

from pickle import NONE
from types import ModuleType
import discord
import random
from discord.ext import commands
from datetime import datetime

#bot = commands.Bot(command_prefix = "!", help_command=None) 
#This file is currently a cog of another file!
# command prefix (it can be changed to any symbol)


class CommandCog(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content == "Listening?":
            await msg.channel.send("I am here!")


    #reply test
    @commands.command()        
    async def test(self,ctx):
        await ctx.send("Here!") 

    #coinflip game
    @commands.command()
    async def coinflip(self,ctx):
        num = random.randint(1,2)

        if num == 1:
            await ctx.send("Heads!")
        if num == 2:
            await ctx.send("Tails!")


    #rock scissors paper game
    @commands.command()
    async def rps(self,ctx, hand):
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


    #help commands
    #displays a box for explanation of each command that bot can handle
    @commands.command(aliases = ["about"]) #aliases is used for alternative usage ex. !help same as !about
    async def help(self,ctx):
        MyEmbed = discord.Embed(title = "Commands", description = "Commands to use for Kebab Bot", color = discord.Colour.dark_magenta())
        MyEmbed.set_thumbnail(url = "https://i.ytimg.com/vi/HfFx5UvzSxc/maxresdefault.jpg")
        MyEmbed.add_field(name = "!ping", value = "Says pong to you!", inline=False)
        MyEmbed.add_field(name = "!coinflip", value = "Play coinflip!", inline=False)
        MyEmbed.add_field(name = "!rps", value = "Play rock scissors paper!", inline=False)
        await ctx.send(embed = MyEmbed)


    @commands.group()
    async def edit(self,ctx):
        pass

    #change server name
    @edit.command()
    async def servername(self,ctx,*, input):
        await ctx.guild.edit(name = input)

    #create a text channel
    @edit.command()
    async def createtextchannel(self,ctx,*, input):
        await ctx.guild.create_text_channel(name = input)

    #create a voice channel
    @edit.command()
    async def createvoicechannel(self,ctx,*, input):
        await ctx.guild.create_voice_channel(name = input)

    #create a role
    @edit.command()
    async def createrole(self,ctx,*, input):
        await ctx.guild.create_role(name = input)

    #kick a user (WARNING! permission may be needed for some roles)
    @commands.command()
    async def kick(self,ctx, member : discord.Member, *, reason = None):
        await ctx.guild.kick(member, reason = reason)

    #ban a user (WARNING! permission may be needed for some roles)
    @commands.command()
    async def ban(self,ctx, member : discord.Member, *, reason = None):
        await ctx.guild.ban(member, reason = reason)

    #unban a user (WARNING! permission may be needed for some roles)
    @commands.command()
    async def unban(self,ctx,*,input):
        name, discriminator = input.split("#")
        banned_members = await ctx.guild.bans()
        for bannedmember in banned_members:
            username = bannedmember.user.name
            disc = bannedmember.user.discriminator
            if name == username and discriminator == disc:
                await ctx.guild.unban(bannedmember.user)


    #delete messages from a text channel, format must be: !purge [number] or !purge [date]
    @commands.command()
    async def purge(self,ctx, amount, day = None, month : int = None, year : int = datetime.now().year):
        if amount == "/":
            if day == None or month == None:
                return
            else:
                await ctx.channel.purge(after = datetime(year, month, day))
        else:
            await ctx.channel.purge(limit = int(amount)+1)


def setup(bot):
    bot.add_cog(CommandCog(bot))
    

#bot.run("TOKEN")  
#This file is currently a cog of another file!
# #replace TOKEN with token id of bot