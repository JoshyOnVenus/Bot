# Import Neccesary Libraries

import json
import logging
import os
import platform
import random
import sys

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()

class LoggingFormatter(logging.Formatter):
    
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

logging_dir = "/home/joshy/Bot"
logging_file = "discord.log"
logging_path = os.path.join(logging_dir, logging_file)

if not os.path.exists(logging_dir):
    os.makedirs(logging_dir)

# File Handler
file_handler = logging.FileHandler(
    filename = logging_path,
    encoding = "utf-8",
    mode = "w"
)
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}",
    style = "{"
)
file_handler.setFormatter(file_handler_formatter)

# Add The Handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class Bot(commands.bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix = commands.when_mentioned_or(config["PREFIX"]),
            intents = intents,
            help_command = None
        )
        self.logger = logger
        self.config = config
        self.database = None
load_dotenv()

bot = Bot()
bot.run(os.getenv("TOKEN"))