import datetime
import asyncio
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import config

discord.utils.setup_logging()

intents = discord.Intents.all()
intents.message_content = True

load_dotenv()

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="TFR Requests..."))
    print(f'User: {bot.user.name} \n ID: {bot.user.id}')
    try:
        await bot.tree.sync(guild=discord.Object(id=1204556647373086790))
    except Exception as e:
        print(e)
    info_channel = bot.get_channel(1219063853476741270)
    await info_channel.send(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] - I am alive!")

# @bot.event
# async def on_error(event, *args, **kwargs):
#     print('An error occurred:', args[0])
    
async def load_cogs():
    for cog in os.listdir('/home/joshy/Bot/cogs'):
        if cog.endswith('_cog.py'):
            module = cog[:-3]
            await bot.load_extension(f'cogs.{module}')

async def main():
    async with bot:
        await load_cogs()
        try:
            print("Starting bot...")
            await bot.start(os.getenv("TOKEN"))
        except discord.ClientConnectionError:
            print("Connection Error!")
            await asyncio.sleep(10)

asyncio.run(main())
