import queue
from turtle import title
import discord
from discord.ext import commands, tasks
import time
import datetime
import os
import asyncio
import re
import random
import urllib
import urllib.request
import requests
from dotenv import load_dotenv
from discord.utils import get   
from discord import FFmpegPCMAudio
from discord import TextChannel
import youtube_dl
from pytube import YouTube
from discord.voice_client import VoiceClient
from random import choice


intents = discord.Intents.default()
intents.members = True
bot_activity = activity=discord.Game(name="~도움 | Developing now...")

bot = commands.Bot(command_prefix='~', status = discord.Status.online, activity = bot_activity, help_command=None, intents=intents) # status: online, idle, dnd, invisible, offline


@bot.event
async def on_ready():
    print("Dosiyo DEV 봇이 시작되었습니다.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
    	await ctx.send("명령어를 찾지 못했어요")




####################################################################################################
# service funsion
####################################################################################################

@bot.command()
async def 서버정보(ctx):
    embed = discord.Embed(title="반갑습니다 {}님! \n{} 서버의 구성원은 총 {} 명이고 \n어드민은 {} 입니다.".format(ctx.author.name, ctx.guild.name, ctx.guild.member_count, ctx.guild.owner.name), color = 0xffcfcf)
    embed.set_image(url = ctx.guild.icon_url)
    await ctx.send(embed=embed)


@bot.command()
async def 주사위(ctx):
    dice = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:']
    num = random.choice(dice)

    embed = discord.Embed(title = "주사위 결과", color = 0xffcfcf)
    embed.add_field(name =  num, value = "라고하네요", inline = False)
    embed.set_footer(text="굴려굴려")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1013779830120136825/1013835951182712842/images.png")
    await ctx.send(embed=embed)


@bot.command()
async def 검색(ctx):
    msg = ctx.message.content[4:]
    await ctx.send('구글: {} \n\n유튜브: {}'.format('https://www.google.com/search?q=' + msg + '&oq=' + msg + '&aqs=chrome..69i57j0l6j69i61.4099j0j7&sourceid=chrome&ie=UTF-8', 'https://www.youtube.com/results?search_query=' + msg))


@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title = """**반가워요! 전 '하와와 도시요'라고 해요!**""", color = 0xffcfcf)

    embed.add_field(name = """모든 명령어 앞에는 '~'가 붙어요""", value = "ex) `~프로필`")
    embed.add_field(name = "아래에서 제가 아는 모든 명령어를 볼 수 있어요!", value = "~~아직 작성중~~", inline = False)
    embed.add_field(name = "추가하고싶은 기능이나 도움이 필요한 부분이 있으면 \nDosiyo DEV 서버에 들어오세요!", value = "https://discord.gg/X6NvyWrsR5", inline = False)

    embed.set_footer(text="Bot made by. 쫑미")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/1013779830120136825/1013779902174081054/e5a3c19f80db5346.png")
    await ctx.send(embed=embed)


@bot.command()
async def 프로필(ctx):
        date = datetime.datetime.utcfromtimestamp(((int(ctx.author.id) >> 22) + 1420070400000) / 1000)
        embed = discord.Embed(color=0xffcfcf)
        embed.add_field(name = "**이름**", value = ctx.author.name, inline=True)
        embed.add_field(name = "**서버닉네임**", value = ctx.author.nick, inline=True)
        embed.add_field(name = "**디스코드가입일**", value = str(date.year) + "년 " + str(date.month) + "월 " + str(date.day) + "일", inline=True)
        embed.add_field(name = "**아이디**", value = ctx.author.id, inline=True)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        await ctx.send(embed=embed)


@bot.command()
async def 안녕(ctx):
        await ctx.send("안녕하세요")




####################################################################################################
# music funsion
####################################################################################################

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

def is_connected(ctx):
    voice_bot = ctx.message.guild.voice_bot
    return voice_bot and voice_bot.is_connected()

# bot = commands.Bot(command_prefix='?')

status = ['Jamming out to music!', 'Eating!', 'Sleeping!']
queue = []
loop = False

@bot.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(bot.latency * 1000)}ms')

@bot.command(name='hello', help='This command returns a random welcome message')
async def hello(ctx):
    responses = ['***grumble*** Why did you wake me up?', 'Top of the morning to you lad!', 'Hello, how are you?', 'Hi', '**Wasssuup!**']
    await ctx.send(choice(responses))

@bot.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = ['why have you brought my short life to an end', 'i could have done so much more', 'i have a family, kill them instead']
    await ctx.send(choice(responses))

@bot.command(name='credits', help='This command returns the credits')
async def credits(ctx):
    await ctx.send('Made by `RK Coding`')
    await ctx.send('Thanks to `DiamondSlasher` for coming up with the idea')
    await ctx.send('Thanks to `KingSticky` for helping with the `?die` and `?creditz` command')

@bot.command(name='creditz', help='This command returns the TRUE credits')
async def creditz(ctx):
    await ctx.send('**No one but me, lozer!**')

@bot.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()
    
@bot.command(name='leave', help='This command stops the music and makes the bot leave the voice channel')
async def leave(ctx):
    voice_bot = ctx.message.guild.voice_bot
    await voice_bot.disconnect()

@bot.command(name='loop', help='This command toggles loop mode')
async def loop_(ctx):
    global loop

    if loop:
        await ctx.send('Loop mode is now `False!`')
        loop = False
    
    else: 
        await ctx.send('Loop mode is now `True!`')
        loop = True

@bot.command(name='play', help='This command plays music')
async def play(ctx):
    global queue

    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    try: await channel.connect()
    except: pass

    server = ctx.message.guild
    voice_channel = server.voice_bot
    
    try:
        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=bot.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            
            if loop:
                queue.append(queue[0])

            del(queue[0])
            
        await ctx.send('**Now playing:** {}'.format(player.title))

    except:
        await ctx.send('Nothing in your queue! Use `?queue` to add a song!')

@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_bot

    voice_channel.pause()

@bot.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_bot

    voice_channel.resume()

@bot.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_bot

    voice_channel.stop()

@bot.command(name='queue')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')

@bot.command(name='remove')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')

@bot.command(name='view', help='This command shows the queue')
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')

@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))




####################################################################################################
# server manage funsion
####################################################################################################

# if ctx.author != ctx.guild.owner:
#     await ctx.send("이 명령어는 서버 관리자만 사용할 수 있어요")
#     return None

@bot.command()
async def clear(ctx):
    if ctx.author != ctx.guild.owner:
        await ctx.send("이 명령어는 서버 관리자만 사용할 수 있어요")
        return None

    amount = int(ctx.message.content[7:]) + 1
    await ctx.channel.purge(limit = amount)
    await ctx.send("메세지를 청소했어요")
    time.sleep(1)
    await ctx.channel.purge(limit = 1)




bot.run('OTg0NTYxMDU3ODQ4Nzc4Nzky.GDgBxL.vvXmIYWSXZ291ZkJSlU1n2WotVY22abeEPJbmI')