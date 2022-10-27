# This example requires the 'message_content' intent.
import asyncio
import os
from datetime import datetime, timedelta

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="config")


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents)

channel_id = 1035117968054566955

@bot.command('today')
async def send_game(ctx):
    if ctx.channel == bot.get_channel(channel_id):
        await ctx.channel.send('test')

    
async def schedule_daily_new_game():
    while True:
        now = datetime.now()
        then = now + timedelta(days=1)
        then.replace(hour=7,minute=0,second=0)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)
        channel = bot.get_channel(channel_id)
        await channel.send('Message Test')  # type: ignore


@bot.event
async def on_ready():
    print("Bot ready : {0.user}".format(bot))
    await schedule_daily_new_game()
    


bot.run(os.getenv("TOKEN"))  # type: ignore