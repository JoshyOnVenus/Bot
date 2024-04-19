import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from utils import Color

# Here we name the cog and create a new class for the cog.
class Owner(commands.Cog, name = "owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name = "sync", description = "Synchronizes the slash commands.")
    @app_commands.describe(scope = "The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchronizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """
        try:
            if scope == "global":
                await context.bot.tree.sync()
                embed = discord.Embed(
                    description = "Slash commands have been globally synchronized.",
                    color = Color.FELIX
                )
                await context.send(embed = embed)
                return
            elif scope == "guild":
                context.bot.tree.copy_global_to(guild = context.guild)
                await context.bot.tree.sync(guild = context.guild)
                embed = discord.Embed(
                    description = "Slash commands have been synchronized in this guild.",
                    color = Color.FELIX
                )
                await context.send(embed = embed)
                return
        except Exception as e:
            embed = discord.Embed(
                description = f"There was an error trying to sync commands, with reason(s)\n``{e}``",
                color = Color.RED
            )
        await context.send(embed = embed)

    @commands.command(name = "unsync", description = "Unynchronizes the slash commands.")
    @app_commands.describe(scope = "The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Unsynchronizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global`, `current_guild` or `guild`.
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild = None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description = "Slash commands have been globally unsynchronized.",
                color = Color.FELIX
            )
            await context.send(embed = embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild = context.guild)
            await context.bot.tree.sync(guild = context.guild)
            embed = discord.Embed(
                description = "Slash commands have been unsynchronized in this guild.",
                color = Color.FELIX
            )
            await context.send(embed = embed)
            return
        if scope == None or not scope:
            embed = discord.Embed(
                description = "The scope must be `global` or `guild`.", 
                color = Color.RED
            )
        await context.send(embed = embed)
        
    @commands.command(name = "reload", description = "Reloads the bot's cogs.")
    @commands.is_owner()
    async def reload(self, context: Context) -> None:
        """
        Realods the bot's cogs.
        
        :param context: The command context.
        """
        
        try:
            reloaded_cogs = []
            for cog in context.bot.cogs.copy():
                await context.bot.reload_extension(f"cogs.{cog}")
                reloaded_cogs.append(cog)
            embed = discord.Embed(
                description = f"Successfully reloaded all cogs.\n```{', '.join([cog.capitalize() for cog in reloaded_cogs])}```",
                color = Color.FELIX
            )
        except Exception as e:
            embed = discord.Embed(
                description = f"There was an error trying to reload cogs, with reason(s)\n``{e}``",
                color = Color.RED
            )
        await context.send(embed = embed)
    
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
