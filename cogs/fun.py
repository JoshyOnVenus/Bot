import random

import asyncio
import aiohttp
import html
import discord
from discord.ext import commands
from discord.ext.commands import Context
#from discord.ui import Select, SelectOption

from utils import Color
import datetime

# Here we name the cog and create a new class for the cog.
class Fun(commands.Cog, name = "fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name = "fact", description = "Get a random fact.")
    async def fact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        description = data["text"],
                        color = Color.FELIX 
                    )
                else: 
                    embed = discord.Embed(
                        description = "There is something wrong with the API, please try again later.",
                        color = Color.RED
                    )
                await context.send(embed = embed)

    @commands.hybrid_command(name = "joke", description = "Get a random joke.")
    async def joke(self, context: Context) -> None:
        """
        Get a random joke.

        :param context: The hybrid command context.
        """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit") as request:
                if request.status == 200:
                    data = await request.json()
                    if data["type"] == "single":
                        embed = discord.Embed(
                            description = data["joke"],
                            color = Color.FELIX 
                        )
                    else:
                        embed = discord.Embed(
                            description = f"{data['setup']}\n \n{data['delivery']}",
                            color = Color.FELIX 
                        )
                else: 
                    embed = discord.Embed(
                        description = "There is something wrong with the API, please try again later.",
                        color = Color.RED
                    )
                await context.send(embed = embed)

    @commands.hybrid_command(name = "dadjoke", description = "Get a random dadjoke.")
    async def dadjoke(self, context: Context) -> None:
        """
        Get a random dadjoke.

        :param context: The hybrid command context.
        """

        async with aiohttp.ClientSession(headers = {'Accept': 'application/json'}) as session:
            async with session.get("https://icanhazdadjoke.com/") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        description = data["joke"],
                        color = Color.FELIX 
                    )
                else: 
                    embed = discord.Embed(
                        description = "There is something wrong with the API, please try again later.",
                        color = Color.RED
                    )
                await context.send(embed = embed)
    
    @commands.hybrid_command(name = "trivia", description = "Get asked questions, answer them correctly.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def trivia(self, context: Context) -> None:
        """
        Get asked questions, asnwer them correctly
        
        :param context: The hybrid command context.
        """
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get("https://opentdb.com/api.php?amount=1&type=multiple") as request:
                    data = await request.json()
                    answers = [html.unescape(incorrect_answer) for incorrect_answer in data['results'][0]['incorrect_answers']] + [html.unescape(data['results'][0]['correct_answer'])]
                    random.shuffle(answers)
                    nl = '\n'
                    embed = discord.Embed(
                        title = f"{html.unescape(data['results'][0]['question'])}",
                        description = f"_Reply to this message to answer_\n\n``{nl.join(answers)}``",
                        color = Color.FELIX
                    )
                            
                    trivia_msg = await context.send(embed = embed)
                                
                    try:
                        
                        def check(message):
                            if message.author.bot or message.reference is None:
                                return False
                            elif message.channel == context.channel and message.reference.message_id == trivia_msg.id:
                                return True
                        
                        response = await context.bot.wait_for('message', timeout = 20.0, check = check)
                                
                        if response.content.lower() == html.unescape(data['results'][0]['correct_answer']).lower():
                            await response.reply(f"You got the answer of ``{html.unescape(data['results'][0]['correct_answer'])}`` correct!")
                            return
                        else:
                            await context.send(f"The correct answer was: ``{html.unescape(data['results'][0]['correct_answer'])}``")
                            return
                                    
                    except asyncio.TimeoutError:
                        await context.send(f"Time's up! The correct answer was: ``{html.unescape(data['results'][0]['correct_answer'])}``")
                        
            except Exception as e:
                embed = discord.Embed(
                    description = f"There is something wrong, with reason(s)\n``{e}``",
                    color = Color.RED
                )
                await context.send(embed = embed, ephemeral = True)
    
    @commands.hybrid_command(name = "cat", description = "Get a random image of a cat.")
    async def cat(self, context: Context) -> None:
        """
        Get a random image of a cat.
        
        :param context: The hybrid command context.
        """
        
        async with aiohttp.ClientSession(headers = {"x-api-key": f"{self.bot.config['CAT_API_key']}"} ) as session:
            async with session.get("https://api.thecatapi.com/v1/images/search") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        color = Color.FELIX
                    )
                    embed.set_image(url = data[0]['url'])
                else:
                    embed = discord.Embed(
                        description = "There is something wrong with the API, please try agian later.",
                        color = Color.RED
                    )
                await context.send(embed = embed)
                
    @commands.hybrid_command(name = "dog", description = "Get a random image of a dog.")
    async def dog(self, context: Context) -> None:
        """
        Get a random image of a dog.
        
        :param context: The hybrid command context.
        """
        
        async with aiohttp.ClientSession(headers = {"x-api-key": f"{self.bot.config['DOG_API_key']}"} ) as session:
            async with session.get("https://api.thedogapi.com/v1/images/search") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        color = Color.FELIX
                    )
                    embed.set_image(url = data[0]['url'])
                else:
                    embed = discord.Embed(
                        description = "There is something wrong with the API, please try agian later.",
                        color = Color.RED
                    )
                await context.send(embed = embed)
                
    @commands.hybrid_command(name = "weather", description = "Get the weather of a chosen location.")
    async def weather(self, context: Context, *, location: str) -> None:
        """
        Get the weather of a chosen location
        
        :param context: The hybrid command context
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.bot.config['WEATHER_API_key']}&units=metric") as request:
                try:
                    data = await request.json()
                    embed = discord.Embed(
                        description = f"Sunrise: <t:{data['sys']['sunrise']}:R>\nSunset: <t:{data['sys']['sunset']}:R>",
                        color = Color.FELIX,
                        timestamp = datetime.datetime.utcfromtimestamp(data['dt'])
                    )
                    embed.add_field(
                        name = f"Temperature",
                        value = f"Current: {data['main']['temp']}°C ({( data['main']['temp'] * 1.8) + 32}℉)\nHigh: {data['main']['temp_max']}°C ({( data['main']['temp_max'] * 1.8 ) + 32}℉)\nLow: {data['main']['temp_min']}°C ({( data['main']['temp_min'] * 1.8) + 32}℉)"
                    )
                    embed.add_field(
                        name = f"Wind",
                        value = f"Speed: {data['wind']['speed']}m/s ({round((data['wind']['speed'] * 2.23693629), 2)}mph)\nGust: {data['wind']['gust'] if 'gust' in data['wind'] else 'N/A'}m/s ({round((data['wind']['gust'] * 2.23693629), 2) if 'gust' in data['wind'] else 'N/A'}mph)"
                    )
                    embed.set_author(
                        name = f"{data['name']}, {data['sys']['country']}"
                    )
                    embed.set_thumbnail(
                        url = f"http://openweathermap.org/img/w/{data['weather'][0]['icon']}.png"
                    )
                except Exception as e:
                    embed = discord.Embed(
                        description = f"There is something wrong with the API, with reason(s)\n``{e}``",
                        color = Color.RED
                    )
                await context.send(embed = embed)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
