import asyncio
import os
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from dotenv import load_dotenv

from scrape_daily_release import GameReleaseScraper, Game

load_dotenv(dotenv_path="config")


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents)

channel_id = 1035117968054566955

@bot.command('today')
async def send_today_game(ctx):
    if ctx.channel == bot.get_channel(channel_id):
        todays_game = ''
        game_list = GameReleaseScraper.getGamePerDay(str(datetime.now().day))
        if game_list != [] :
            for game in game_list:
                todays_game += str(game) + '\n'
        else:
            todays_game = 'Pas de nouveau jeu demain'        
        await ctx.channel.send(todays_game)

@bot.command('tomorrow')
async def send_tomorrow_game(ctx):
    if ctx.channel == bot.get_channel(channel_id):
        game_this_day = ''
        game_list = GameReleaseScraper.getGamePerDay(str(datetime.now().day + 1))
        if game_list != [] :
            for game in game_list:
                game_this_day += str(game) + '\n'
        else:
            game_this_day = 'Pas de nouveau jeu demain'        
        await ctx.channel.send(game_this_day)

@bot.command('week')
async def send_week_game(ctx):
    if ctx.channel == bot.get_channel(channel_id):
        game_this_week = ''
        game_list = GameReleaseScraper.getGameNextWeek()
        if game_list != [] :
            for game in game_list:
                game_this_week += str(game) + '\n\n'
                '''Check length to avoid bot message length restriction'''
                if(len(game_this_week) > 1500):
                    await ctx.channel.send(game_this_week)
                    game_this_week = ''
        else:
            game_this_week = 'Pas de nouveau jeu cette semaine'        
        await ctx.channel.send(game_this_week)

@bot.command('month')
async def send_month_game(ctx):
    if ctx.channel == bot.get_channel(channel_id):
        game_this_month = ''
        game_list = GameReleaseScraper.getGameActualMonth()
        if game_list != [] :
            for game in game_list:
                game_this_month += str(game) + '\n\n'
                '''Check length to avoid bot message length restriction'''
                if(len(game_this_month) > 1500):
                    await ctx.channel.send(game_this_month)
                    game_this_month = ''
            await ctx.channel.send(str(game_this_month) + '\n')    
        else:
            game_this_month = 'Pas de nouveau jeu ce mois-ci'        
    
async def schedule_daily_new_game():
    while True:
        now = datetime.now()
        then = now + timedelta(days=1)
        then.replace(hour=7,minute=30,second=0)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)
        channel = bot.get_channel(channel_id)
        todays_game = ''
        for game in GameReleaseScraper.getGamePerDay((str(datetime.now()))): 
            todays_game += str(game) + '\n'
        await channel.send(todays_game)  # type: ignore


@bot.event
async def on_ready():
    print("Bot ready : {0.user}".format(bot))
    await schedule_daily_new_game()
    

bot.run(os.getenv("TOKEN"))  # type: ignore