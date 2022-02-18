from importlib.metadata import files
from turtle import title
import discord
from discord.ext import commands

import youtube_dl #there is a problem with extract_info youtube_dl is used for that!
import yt_dlp

import os, asyncio
bot = commands.Bot(command_prefix="!!!")


queuelist = []
filestodelete = []

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, *, searchword):
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

    def check_queue():
        try:
            if queuelist[0] != None:
                voice.play(discord.FFmpegPCMAudio(f"{queuelist[0]}.mp3"), after = lambda e : check_queue())
                filestodelete.append(queuelist[0])
                queuelist.pop(0)
        except IndexError:
            for file in filestodelete:
                os.remove(f"{file}.mp3")
            filestodelete.clear()

    @bot.command()
    async def pausesong(ctx):
        if ctx.voice_client.is_playing() == True:
            ctx.voice_client.pause()
        else:
            await ctx.send("Bot is not playing audio")

    @bot.command(aliases = ["skip"])
    async def stop(ctx):
        if ctx.voice_client.is_playing() == True:
            ctx.voice_client.stop()
        else:
            await ctx.send("Bot is not playing audio")


    @bot.command()
    async def resume(ctx):
        if ctx.voice_client.is_playing() == True:
            await ctx.send("Bot is playing audio!")
        else:
            ctx.voice_client.resume()


    @bot.command()
    async def viewqueue(ctx):
        await ctx.send(f"Queue: {str(queuelist)}")



bot.run("TOKEN")