import discord
intents = discord.Intents.all()
bot = discord.Client(intents = intents)

@bot.event
async def on_ready():
    print("BOT IS ONLINE")

@bot.event
async def on_message(msg):
    username = msg.author.display_name
    if msg.author == bot.user:
        return 
    else:
        if msg.content == "Pardon orası engelli otoparkı":
            await msg.channel.send(username + " ben lol oynuyorum")


@bot.event
async def on_member_join(member):
    guild = member.guild
    guildname = guild.name
    dmchannel = await member.create_dm()
    await dmchannel.send(f"welcome to {guildname}!")


@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    member = payload.member
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    
    if (emoji == "🇦🇱" or emoji == "🇹🇷" or emoji == "🇬🇷" or emoji == "🇭🇷" or emoji == "🇧🇬" or emoji == "🇷🇸") and message_id == 935931466859294731:
        role = discord.utils.get(guild.roles, name = "Balkan")
        await member.add_roles(role)

    if  emoji == "💩" and message_id == 935931535297757214:
        role = discord.utils.get(guild.roles, name = "Non-Balkan")
        await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    user_id = payload.user_id
    emoji = payload.emoji.name
    message_id = payload.message_id
    guild_id = payload.guild_id
    guild = bot.get_guild(guild_id)
    member = guild.get_member(user_id)

    if (emoji == "🇦🇱" or emoji == "🇹🇷" or emoji == "🇬🇷" or emoji == "🇭🇷" or emoji == "🇧🇬" or emoji == "🇷🇸") and message_id == 935931466859294731:
         role = discord.utils.get(guild.roles, name = "Balkan")
         await member.remove_roles(role)
    
    if  emoji == "💩" and message_id == 935931535297757214:
        role = discord.utils.get(guild.roles, name = "Non-Balkan")
        await member.remove_roles(role)


bot.run("OTM1OTEwMjg4MDMxNjIxMTUx.YfFgYQ.ds4HLvh4yBNWQKgONAtYqScG1ng")

