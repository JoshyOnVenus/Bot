import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact..

        :param context: The hybrid command context.
        """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(
                        description = data["text"],
                        color = 0xD75BF4    
                    )
                else: 
                    embed = discord.Embed(
                        title = "Error!",
                        description = "There is something wrong with the API, please try again later.",
                        color = 0xE02B2B
                    )
                    await context.send(embed = embed) 


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))