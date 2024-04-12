import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


# Here we name the cog and create a new class for the cog.
class Owner(commands.Cog, name = "owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name = "sync", description = "Synchonizes the slash commands.")
    @app_commands.describe(scope = "The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description = "Slash commands have been globally synchronized.",
                color = 0xBEBEFE
            )
            await context.send(embed = embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild = context.guild)
            await context.bot.tree.sync(guild = context.guild)
            embed = discord.Embed(
                description = "Slash commands have been synchronized in this guild.",
                color = 0xBEBEFE
            )
            await context.send(embed = embed)
            return
        embed = discord.Embed(
            description = "The scope must be `global` or `guild`.", 
            color=0xE02B2B
        )
        await context.send(embed = embed)

    @commands.command(name = "unsync", description = "Unynchonizes the slash commands.")
    @app_commands.describe(scope = "The scope of the sync. Can be `global`, `current_guild` or `guild`")
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Unsynchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global`, `current_guild` or `guild`.
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild = None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description = "Slash commands have been globally unsynchronized.",
                color = 0xBEBEFE,
            )
            await context.send(embed = embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild = context.guild)
            await context.bot.tree.sync(guild = context.guild)
            embed = discord.Embed(
                description = "Slash commands have been unsynchronized in this guild.",
                color = 0xBEBEFE
            )
            await context.send(embed = embed)
            return
        embed = discord.Embed(
            description = "The scope must be `global` or `guild`.", 
            color = 0xE02B2B
        )
        await context.send(embed = embed)

    
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))