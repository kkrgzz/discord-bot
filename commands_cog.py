"""
Bot Commands for Discord Bot
Play Music Feature
Further updates will be included soon.
"""

from pickle import NONE
from types import ModuleType
import discord
from discord.ext import commands
import random
import os, asyncio
from datetime import datetime

from turtle import title
from importlib.metadata import files
import youtube_dl #there is a problem with extract_info! youtube_dl is used for that.
import yt_dlp

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



    """
    MUSIC BOT CODES STARTS
    """

    queuelist = []
    filestodelete = []

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


    @commands.command()
    async def play(self, ctx, *, searchword):
        ydl_opts = {}
        voice = ctx.voice_client

        #get the title and url from video

        if searchword[0:4] == "http" or searchword[0:3] == "www":
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(searchword, download = False)
                title = info["title"]
                url = searchword

        if searchword[0:4] != "http" and searchword[0:3] != "www":
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{searchword}", download = False)["entries"][0]
                title = info["title"]
                url = info["webpage_url"]

        ydl_opts = {
            'format' : 'bestaudio/best',
            "outtmpl" : f"{title}.mp3",
            "postprocessors":
            [{"key" : "FFmpegExtractAudio", "preferredcodec" : "mp3", "preferredquality" : "192"}],
        }



        def download(url):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, download, url)


        #playing and queueing audio
        if voice.is_playing():
            queuelist.append(title)
            await ctx.send(f"Added to queue: {title}")
        else:
            voice.play(discord.FFmpegPCMAudio(f"{title}.mp3"), after = lambda e : check_queue())
            await ctx.send(f"Playing {title} !!!")
            filestodelete.append(title)

        def check_queue(self):
            try:
                if queuelist[0] != None:
                    voice.play(discord.FFmpegPCMAudio(f"{queuelist[0]}.mp3"), after = lambda e : check_queue())
                    filestodelete.append(queuelist[0])
                    queuelist.pop(0)
            except IndexError:
                for file in filestodelete:
                    os.remove(f"{file}.mp3")
                filestodelete.clear()

        @commands.command()
        async def pausesong(self, ctx):
            if ctx.voice_client.is_playing() == True:
                ctx.voice_client.pause()
            else:
                await ctx.send("Bot is not playing audio")

        @commands.command(aliases = ["skip"])
        async def stop(self, ctx):
            if ctx.voice_client.is_playing() == True:
                ctx.voice_client.stop()
            else:
                await ctx.send("Bot is not playing audio")


        @commands.command()
        async def resume(self, ctx):
            if ctx.voice_client.is_playing() == True:
                await ctx.send("Bot is playing audio!")
            else:
                ctx.voice_client.resume()


        @commands.command()
        async def viewqueue(self, ctx):
            await ctx.send(f"Queue: {str(queuelist)}")


def setup(bot):
    bot.add_cog(CommandCog(bot))



#bot.run("TOKEN")
#This file is currently a cog of another file!
# #replace TOKEN with token id of bot
