# Import Necessary Libraries

# Operating System Interaction
import os
import platform
import sys

# Data Handling
import json
from dotenv import load_dotenv
import aiosqlite
from database import DatabaseManager

# Logging
import logging
from utils import LoggingFormatter, Color

# Discord
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

# Other
import random


if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()

intents.message_content = True

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

# File Handler
logging_dir = "/home/joshy/Bot"
logging_file = "discord.log"
logging_path = os.path.join(logging_dir, logging_file)

if not os.path.exists(logging_dir):
    os.makedirs(logging_dir)

file_handler = logging.FileHandler(
    filename = logging_path,
    encoding = "utf-8",
    mode = "w"
)
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}",
    "%Y-%m-%d %H:%M:%S",
    style = "{"
)
file_handler.setFormatter(file_handler_formatter)

# Add The Handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix = commands.when_mentioned_or(config["PREFIX"]),
            intents = intents,
            help_command = None
        )
        self.logger = logger
        self.config = config
        self.database = None
    
    async def init_db(self) -> None:
        async with aiosqlite.connect(f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db") as db:
            with open(f"{os.path.realpath(os.path.dirname(__file__))}/database/schema.sql") as file:
                await db.executescript(file.read())
            await db.commit()
    
    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded Extension: {extension}")
                    self.logger.info(f"     - {', '.join([command.name for command in self.get_cog(extension).walk_commands()])}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(f"Failed To Load Extension: {extension}\n{exception}")
                    
    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
        statuses = ["SpaceX", "TFRs", "with you!"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))

    @status_task.before_loop
    async def before_status_task(self) -> None:
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        self.logger.info(f"Logged In As: {self.user.name}")
        self.logger.info(f"Discord.py API Version: {discord.__version__}")
        self.logger.info(f"Python Version: {platform.python_version()}")
        self.logger.info(f"Running On: {platform.system()} {platform.release()} ({os.name})")
        self.logger.info("-------------------")
        await self.init_db()
        await self.load_cogs()
        self.status_task.start()
        self.database = DatabaseManager(
            connection = await aiosqlite.connect(f"{os.path.realpath(os.path.dirname(__file__))}/database/database.db")
        )

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(f"Excecuted {executed_command} command in {context.guild.name} by {context.author} (ID: {context.author.id})")
        else:
            self.logger.info(f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

    async def on_command_error(self, context: Context, error) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description = f"**Please Slow Down!** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color = Color.RED
            )
            await context.send(embed = embed, ephemeral = True)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description = "You are not the owner of this bot!",
                color = Color.RED
            )
            await context.send(embed = embed)

            if context.guild:
                self.logger.warning(f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot.")
            else:
                self.logger.warning(f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is no an owner of the bot.")
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description = "You are missing the permission(s) `" + ", ".join(error.missing_permissions) + "` to execute this command!",
                color = Color.RED
            )
            await context.send(embed = embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description = "I am missing the permission(s) `" + ", ".join(error.missing_permissions) + "` to fully perform this command!",
                color = Color.RED
            )
            await context.send(embed = embed)
        else:
            raise error

load_dotenv()

bot = Bot()
bot.run(os.getenv("TOKEN"))
