import queue
from turtle import title
import discord
from discord.ext import commands
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
from youtube_dl import YoutubeDL
from pytube import YouTube


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

load_dotenv()
link_queue = []
title_queue = []

@bot.command(aliases = ['join', 'j', 'ㅓ'])
async def Join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


@bot.command(aliases = ['play', 'p', 'ㅔ'])
async def Play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)

    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    if not voice.is_playing():
        message = ctx.message.content

        if message.startswith('~play'):
            link = message[6:]

        if message.startswith('~p') or message.startswith('~ㅔ'):
            link = message[3: ]

        link_queue.append(link)

        # with YoutubeDL(YDL_OPTIONS) as ydl:
        #     info = ydl.extract_info(url, download=False)
        URL = link_queue[1] # info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()














    else:
        await ctx.send("Bot is already playing")
        return


@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


@bot.command(aliases = ['skip', 's', 'ㄴ'])
async def Skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()



@bot.command(aliases = ['st'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()


@bot.command(aliases = ['queue', 'q', 'ㅂ'])
async def Queue(ctx):
    await ctx.send(queue)


@bot.command()
async def leave(ctx):
    await bot.voice_clients[0].disconnect()




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




bot.run('OTg0NTYxMDU3ODQ4Nzc4Nzky.GMPLbM.hyP8expOwRSSONA0KaHwungevMTfcXUXuIkMqY')