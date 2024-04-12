import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class General(commands.Cog, name = "general"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name = "help", description = "List of all the bot commands.")
    async def help(self, context: Context) -> None:
        """
        List of all the bot commands.

        :param context: The hybrid command context.
        """
        prefix = self.bot.config["PREFIX"]
        embed = discord.Embed(
            title = "Help",
            description = "List of all the available commands: ",
            color = 0xBEBEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name = i.capitalize(),
                value = f"```{help_text}```",
                inline = False
            )
        await context.send(embed = embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(General(bot))