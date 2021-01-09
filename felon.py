# -*- coding: utf-8 -*-
class SELFBOT():
    __linecount__= 1933
    __version__= 0.1

import asyncio, json, os, random, ctypes, re, string, requests, numpy, time, datetime, sys, discord, colorama, aiohttp
from datetime import datetime, timezone


from colorama import Fore
from pathlib import Path
from sys import platform
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, check, Cog, command, has_guild_permissions
import pyPrivnote as pn
from gtts import gTTS
from discord import Embed, Member

class MissingPermissions(CheckFailure): pass


def has_permissions(**perms):
    def predicate(ctx):
        msg = ctx.message
        ch = msg.channel
        permissions = ch.permissions_for(msg.author)
        if all(getattr(permissions, perm, None) == value for perm, value in perms.items()):
            return True
        raise MissingPermissions()

    return check(predicate)


def get_prefix(client, message):
    with open('config.json', 'r') as f:
        config = json.load(f)

    return config["prefix"]


settings = json.loads(open("./config.json").read())
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=False)
client = commands.Bot(get_prefix, case_insensitive=True, intents=intents, self_bot=True)
color = 0x2f3137
client.remove_command('help')


with open('config.json') as f:
    config = json.load(f)
    token = config.get('token')
    prefix = config.get('prefix')

giveaway_sniper = config.get('giveaway_sniper')
slotbot_sniper = config.get('slotbot_sniper')
nitro_sniper = config.get('nitro_sniper')
privnote_sniper = config.get('privnote_sniper')


colorama.init()


def startprint():
    if giveaway_sniper == True:
        giveaway = "Active" 
    else:
        giveaway = "Disabled"

    if nitro_sniper == True:
        nitro = "Active"
    else:
        nitro = "Disabled"

    if slotbot_sniper == True:
        slotbot = "Active"
    else:
        slotbot = "Disabled"

    if privnote_sniper == True:
        privnote = "Active"
    else:
        privnote = "Disabled" 

    print(f'''{Fore.RED}

                ███████╗███████╗██╗      ██████╗ ███╗   ██╗
                ██╔════╝██╔════╝██║     ██╔═══██╗████╗  ██║
                █████╗  █████╗  ██║     ██║   ██║██╔██╗ ██║
                ██╔══╝  ██╔══╝  ██║     ██║   ██║██║╚██╗██║
                ██║     ███████╗███████╗╚██████╔╝██║ ╚████║
                ╚═╝     ╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
                    {Fore.WHITE}

                {Fore.RED}Prefix: {Fore.LIGHTBLUE_EX}{prefix}
                {Fore.RED}Privnote Sniper | {Fore.LIGHTBLUE_EX}{privnote}
                {Fore.RED}Nitro Sniper | {Fore.LIGHTBLUE_EX}{nitro}
                {Fore.RED}Giveaway Sniper | {Fore.LIGHTBLUE_EX}{giveaway}
                {Fore.RED}SlotBot Sniper | {Fore.LIGHTBLUE_EX}{slotbot}
                {Fore.RED}Logged In As: {Fore.LIGHTBLUE_EX}{client.user.name}#{client.user.discriminator} {Fore.RED}| ID: {Fore.LIGHTBLUE_EX}{client.user.id}

    ''' + Fore.RESET)

def Clear():
    os.system('cls')
Clear()

class Login(discord.Client):
    async def on_connect(self):
        guilds = len(self.guilds)
        users = len(self.users)
        print("")
        print(f"Connected to: [{self.user.name}]")
        print(f"Token: {self.http.token}")
        print(f"Guilds: {guilds}")
        print(f"Users: {users}")
        print("-------------------------------")
        await self.logout()


@client.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CheckFailure):
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}You're missing permission to execute this command"+Fore.RESET)
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Missing arguments: {error}"+Fore.RESET)
    elif isinstance(error, numpy.AxisError):
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Not a valid image"+Fore.RESET)
    elif isinstance(error, discord.errors.Forbidden):
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Discord error: {error}"+Fore.RESET)
    elif "Cannot send an empty message" in error_str:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Couldnt send a empty message"+Fore.RESET)               
    else:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{error_str}"+Fore.RESET)

@client.event
async def on_message_edit(before, after):
    await client.process_commands(after)

@client.event
async def on_message(message):

    def GiveawayData():
        print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"   
    +Fore.RESET)

    def SlotBotData():
        print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]"
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"   
    +Fore.RESET)  

    def NitroData(elapsed, code):
        print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]" 
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
        f"\n{Fore.WHITE} - AUTHOR: {Fore.YELLOW}[{message.author}]"
        f"\n{Fore.WHITE} - ELAPSED: {Fore.YELLOW}[{elapsed}]"
        f"\n{Fore.WHITE} - CODE: {Fore.YELLOW}{code}"
    +Fore.RESET)

    def PrivnoteData(code):
        print(
        f"{Fore.WHITE} - CHANNEL: {Fore.YELLOW}[{message.channel}]" 
        f"\n{Fore.WHITE} - SERVER: {Fore.YELLOW}[{message.guild}]"
        f"\n{Fore.WHITE} - CONTENT: {Fore.YELLOW}[The content can be found at Privnote/{code}.txt]"
    +Fore.RESET)        

    time = datetime.now().strftime("%H:%M %p")  
    if 'discord.gift/' in message.content:
        if nitro_sniper == True:
            start = datetime.now()
            code = re.search("discord.gift/(.*)", message.content).group(1)
            token = config.get('token')
                
            headers = {'Authorization': token}
    
            r = requests.post(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', 
                headers=headers,
            ).text
        
            elapsed = datetime.now() - start
            elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'

            if 'This gift has been redeemed already.' in r:
                print(""
                f"\n{Fore.CYAN}[{time} - Nitro Already Redeemed]"+Fore.RESET)
                NitroData(elapsed, code)

            elif 'subscription_plan' in r:
                print(""
                f"\n{Fore.CYAN}[{time} - Nitro Success]"+Fore.RESET)
                NitroData(elapsed, code)

            elif 'Unknown Gift Code' in r:
                print(""
                f"\n{Fore.CYAN}[{time} - Nitro Unknown Gift Code]"+Fore.RESET)
                NitroData(elapsed, code)
        else:
            return
            
    if 'Someone just dropped' in message.content:
        if slotbot_sniper == True:
            if message.author.id == 346353957029019648:
                try:
                    await message.channel.send('~grab')
                except discord.errors.Forbidden:
                    print(""
                    f"\n{Fore.CYAN}[{time} - SlotBot Couldnt Grab]"+Fore.RESET)
                    SlotBotData()                     
                print(""
                f"\n{Fore.CYAN}[{time} - Slotbot Grabbed]"+Fore.RESET)
                SlotBotData()
        else:
            return

    if 'GIVEAWAY' in message.content:
        if giveaway_sniper == True:
            if message.author.id == 294882584201003009:
                try:    
                    await message.add_reaction("ðﾟﾎﾉ")
                except discord.errors.Forbidden:
                    print(""
                    f"\n{Fore.CYAN}[{time} - Giveaway Couldnt React]"+Fore.RESET)
                    GiveawayData()            
                print(""
                f"\n{Fore.CYAN}[{time} - Giveaway Sniped]"+Fore.RESET)
                GiveawayData()
        else:
            return

    if f'Congratulations <@{client.user.id}>' in message.content:
        if giveaway_sniper == True:
            if message.author.id == 294882584201003009:    
                print(""
                f"\n{Fore.CYAN}[{time} - Giveaway Won]"+Fore.RESET)
                GiveawayData()
        else:
            return

    if 'privnote.com' in message.content:
        if privnote_sniper == True:
            code = re.search('privnote.com/(.*)', message.content).group(1)
            link = 'https://privnote.com/'+code
            try:
                note_text = pn.read_note(link)
            except Exception as e:
                print(e)    
            with open(f'Privnote/{code}.txt', 'a+') as f:
                print(""
                f"\n{Fore.CYAN}[{time} - Privnote Sniped]"+Fore.RESET)
                PrivnoteData(code)
                f.write(note_text)
        else:
            return
    await client.process_commands(message)


@client.event
async def on_connect():
    Clear()

    if giveaway_sniper == True:
        giveaway = "Active" 
    else:
        giveaway = "Disabled"

    if nitro_sniper == True:
        nitro = "Active"
    else:
        nitro = "Disabled"

    if slotbot_sniper == True:
        slotbot = "Active"
    else:
        slotbot = "Disabled"

    if privnote_sniper == True:
        privnote = "Active"
    else:
        privnote = "Disabled"    
    
    startprint()
    ctypes.windll.kernel32.SetConsoleTitleW(f'[Felon Selfbot v{SELFBOT.__version__}] | Logged in as {client.user.name}')


def __init__(self, client):
    self.client = client


@client.command()
async def stream(ctx, *, message):
        await ctx.message.delete()
        stream = discord.Streaming(
            name=message,
            url="https://www.twitch.tv/monstercat",
        )
        await client.change_presence(activity=stream)




@client.command()
async def embed(ctx, *, content: str):
    await ctx.message.delete()
    title, description = content.split('|')
    embed = discord.Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)


@client.command()
async def bot(ctx):
    await ctx.message.delete()
    my_embed = discord.Embed(color=color)

    my_embed.set_author(name="Self Bot Info")

    my_embed.add_field(name="Version Code:\n", value="v0.1", inline=False)

    my_embed.add_field(name="Released On:", value="January 2021", inline=False)


    my_embed.add_field(name="Partner",
                       value=f"[Felon!](https://discord.gg/RW5uMtWTJv)",)


    my_embed.set_footer(text="Made by Cujo")
    my_embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.message.channel.send(embed=my_embed)

@client.command()
async def btc(ctx): # b'\xfc'
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR').json()
    usd = r['USD']
    eur = r['EUR']
    em = discord.Embed(description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`')
    em.set_author(name='Bitcoin', icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png')
    await ctx.send(embed=em)

@client.command()
async def eth(ctx): # b'\xfc'
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR').json()
    usd = r['USD']
    eur = r['EUR']
    em = discord.Embed(description=f'USD: `{str(usd)}$`\nEUR: `{str(eur)}€`')
    em.set_author(name='Ethereum', icon_url='https://cdn.discordapp.com/attachments/271256875205525504/374282740218200064/2000px-Ethereum_logo.png')
    await ctx.send(embed=em)





@client.command(aliases=['pfp'])
async def av(ctx, member: discord.Member = None): # b'\xfc'
    await ctx.message.delete()
    if not member:
        member = ctx.author
    embed = discord.Embed(title="Avatar", color=color)
    embed.set_author(name=f"{member}", icon_url=f'{member.avatar_url}')
    embed.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=embed)


@client.command()
async def help(ctx): # b'\xfc'
    await ctx.message.delete()
    embed = discord.Embed(title="`Commands`", color=color, inline=True)
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    embed.add_field(name="`Info`", value="*Check Info Commands*", inline=False)
    embed.add_field(name="`Fun`", value="*Check Fun Commands*", inline=False)
    embed.add_field(name="`User`", value="*Check User Commands*", inline=False)
    embed.add_field(name="`Raid`", value="*Check Raid Commands*", inline=False)

    embed.set_footer(text='help categories')
    await ctx.send(embed=embed)



@client.command()
async def fun(ctx): # b'\xfc'
    await ctx.message.delete()
    embed = discord.Embed(title="`Fun`", color=color, inline=True)
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    embed.add_field(name="`dog`", value="*Gives you a random dog image ʕ•́ᴥ•̀ʔっ*", inline=False)
    embed.add_field(name="`kiss`", value="*Kiss someone <3*", inline=False)
    embed.add_field(name="`hug`", value="*Hug someone ^.^*", inline=False)
    embed.add_field(name="`slap`", value="*Slap someone </3*", inline=False)
    embed.add_field(name="`feed`", value="*Feed someone -.-*", inline=False)
    embed.add_field(name="`cuddle`", value="*Cuddle with someone ⊂（♡⌂♡）⊃*", inline=False)
    embed.add_field(name="`tickle`", value="*Tickle someone ♡*", inline=False)
    embed.add_field(name="`pat`", value="*Pat someone (ㆆ_ㆆ)*", inline=False)
    embed.add_field(name="`poll`", value="*Start a poll (ง︡'-'︠)ง*", inline=False)
    embed.add_field(name="`joke`", value="*drop a random joke*", inline=False)
    # embed.add_field(name="",value="",inline=False)
    embed.set_footer(text='fun categories')

    await ctx.send(embed=embed)


@client.command()
async def user(ctx): # b'\xfc'
    await ctx.message.delete()
    embed = discord.Embed(title="`User`", color=color, inline=True)
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    embed.add_field(name="`av`", value="*Avatar someone*", inline=False)
    embed.add_field(name="`purge`", value="*Purges amount of messages*", inline=False)
    embed.add_field(name="`snipe`", value="*Snipe a message*", inline=False)
    embed.add_field(name="`embed`", value="*Embed a message, Title | Description*", inline=False)
    embed.add_field(name="`logout`", value="*logout of selfbot*", inline=False)


    # embed.add_field(name="",value="",inline=False)
    embed.set_footer(text='user categories')

    await ctx.send(embed=embed)


@client.command()
async def info(ctx): # b'\xfc'
    await ctx.message.delete()
    embed = discord.Embed(title="`Info`", color=color, inline=True)
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    embed.add_field(name="`serverinfo`", value="*Pull up current server's information*", inline=False)
    embed.add_field(name="`userinfo`", value="*Shows user information*", inline=False)
    embed.add_field(name="`bot`", value="*Gives you self bot information*", inline=False)
    embed.add_field(name="`stream`", value="*Change status to streaming*", inline=False)
    embed.add_field(name="`inv`", value="*Download the selfbot*", inline=False)

    # embed.add_field(name="",value="",inline=False)
    embed.set_footer(text='info categories')
    await ctx.send(embed=embed)

@client.command()
async def raid(ctx): # b'\xfc'
    await ctx.message.delete()
    embed = discord.Embed(title="`Raid`", color=color, inline=True)
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    embed.add_field(name="`nuke`", value="*Deletes channels, roles, and bans members*")

    # embed.add_field(name="",value="",inline=False)
    embed.set_footer(text='Raid categories')
    await ctx.send(embed=embed)

@client.command()
async def crypto(ctx): # b'\xfc'
    await ctx.message.delete()
    embed = discord.Embed(title="`Crypto`", color=color, inline=True)
    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    embed.add_field(name="`eth`", value="*Ethereum price*", inline=False)
    embed.add_field(name="`btc`", value="*Bitcoin price*", inline=False)

    # embed.add_field(name="",value="",inline=False)
    embed.set_footer(text='crypto categories')
    await ctx.send(embed=embed)



@client.command(name='inv')
async def inv(ctx): # b'\xfc'
    await ctx.message.delete()
    print('inv link generated')
    embed = discord.Embed(
        title="Wanna use this selfbot?",
        description=" [__Download!__](https://github.com/itzCujo/Felon)",
        color=color,
        timestamp=datetime.now(),
    )
    embed.set_footer(text="felon")
    await ctx.message.channel.send(embed=embed)

@client.command()
async def userinfo(ctx, member: discord.Member = None): # b'\xfc'
    await ctx.message.delete()
    if not member:
        member = ctx.message.author
    date_format = "%a , %d %b %Y %I:%M %p"
    join_pos = sorted(ctx.guild.members, key=lambda member: member.joined_at).index(member) + 1
    roles = [role for role in member.roles]
    embed = discord.Embed(timestamp=ctx.message.created_at, color=color)
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)

    embed.add_field(name="ID:", value=member.id, inline=False)
    embed.add_field(name="Display Name:", value=member.display_name, inline=False)

    embed.add_field(name="Registered", value=member.created_at.strftime(date_format), inline=False)
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                    inline=False)
    embed.add_field(name="Position:", value=f"{join_pos}/{len(ctx.guild.members)}", inline=False)

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Highest Role:", value=member.top_role.mention, inline=False)
    embed.set_footer(text=f"𝙧𝙚𝙦𝙪𝙚𝙨𝙩𝙚𝙙 𝙗𝙮 {ctx.author.name}", icon_url=ctx.author.avatar_url)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx): # b'\xfc'
    await ctx.message.delete()
    name = ctx.guild.name
    create_server = ctx.guild.created_at
    owner_server = ctx.guild.owner
    server = ctx.message.guild
    role_count = len(server.roles)
    emoji_count = len(server.emojis)
    channel_count = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

    em = discord.Embed(timestamp=ctx.message.created_at, color=color)
    em.set_author(name=str(name), icon_url=ctx.guild.icon_url)
    em.set_thumbnail(url=ctx.guild.icon_url)

    em.add_field(name="Owner", value=owner_server, inline=False)
    em.add_field(name='Region', value=server.region, inline=False)
    em.add_field(name='Members', value=server.member_count, inline=False)
    em.add_field(name="Created On", value=create_server.strftime("%a, %#d %B %Y"), inline=False)
    em.add_field(name='Text Channels', value=str(channel_count), inline=False)
    em.add_field(name='Number of Roles', value=str(role_count))
    em.add_field(name='Number of Emotes', value=str(emoji_count))

    await ctx.send(embed=em)

@client.command()
async def poll(ctx, *, question):
    await ctx.message.delete()
    emoji1 = '✅'
    emoji2 = '❌'
    question = await ctx.send(f'{question}')
    await question.add_reaction(emoji1)
    await question.add_reaction(emoji2)

@client.command()
async def kiss(ctx, user: discord.Member):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/kiss")
    res = r.json()
    em = discord.Embed(description=f'{ctx.author.mention} kisses {user.mention}', color=color)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def dog(ctx): # b'\xfc'
    await ctx.message.delete()
    r = requests.get("https://dog.ceo/api/breeds/image/random").json()
    em = discord.Embed(description=f'woof', color=color)
    em.set_image(url=str(r['message']))
    try:
        await ctx.send(embed=em)
    except:
        await ctx.send(str(r['message']))  

@client.command()
async def pat(ctx, user: discord.Member):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/pat")
    res = r.json()
    em = discord.Embed(description=f'{ctx.author.mention} pats {user.mention}', color=color)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def hug(ctx, user: discord.Member):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/hug")
    res = r.json()
    em = discord.Embed(description=f'{ctx.author.mention} hugs {user.mention}', color=color)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def slap(ctx, user: discord.Member):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/slap")
    res = r.json()
    em = discord.Embed(description=f'{ctx.author.mention} slaps {user.mention}', color=color)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def tickle(ctx, user: discord.Member):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/tickle")
    res = r.json()
    em = discord.Embed(description=f'{ctx.author.mention} tickles {user.mention}', color=color)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def feed(ctx, user: discord.Member):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/feed")
    res = r.json()
    em = discord.Embed(description=f'{ctx.author.mention} feeds {user.mention}', color=color)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def cuddle(ctx, user: discord.Member):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/cuddle")
    res = r.json()
    em = discord.Embed(description=f'{ctx.author.mention} cuddles {user.mention}', color=color)
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

@client.command()
async def joke(ctx):  # b'\xfc'
    await ctx.message.delete()
    headers = {
        "Accept": "application/json"
    }
    async with aiohttp.ClientSession()as session:
        async with session.get("https://icanhazdadjoke.com", headers=headers) as req:
            r = await req.json()
    await ctx.send(r["joke"])


@client.command()
async def purge(ctx, amount: int): # b'\xfc'
    await ctx.message.delete()
    async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == client.user).map(lambda m: m):
        try:
           await message.delete()
        except:
            pass

@client.command()
async def logout(ctx): # b'\xfc'
    await ctx.message.delete()
    await client.logout()


def RandomColor(): 
    randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
    return randcolor

@client.command()
async def nuke(ctx): # b'\xfc'
    await ctx.message.delete()
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()    
        except:
            pass
    for user in list(ctx.guild.members):
        try:
            await user.ban()
        except:
            pass    
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass
    try:
        await ctx.guild.edit(
            name="Felon",
            description=None,
            reason=None,
            icon=None,
            banner=None
        )  
    except:
        pass        
    for _i in range(250):
        await ctx.guild.create_text_channel(name="get nuked")
    for _i in range(250):
        await ctx.guild.create_role(name="get nuked", color=RandomColor())

client.run(token, bot=False)
