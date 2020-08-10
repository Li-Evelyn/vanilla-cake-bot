import os
import discord
import random
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from dotenv import load_dotenv
import Files.spotify as spotify
import Files.gaming as gaming
import Files.youtube as youtube

# env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
MUSIC_CHANNEL = os.getenv("MUSIC_CHANNEL_KEYWORD")

# variables
statuses = [["you", "Netflix", "Re:Zero", "Kakegurui", "basketball", "hockey"],
            ["with fire", "Poker against myself...and losing", "trumpet", "piano", "tennis", "badminton"],
            ["my new mixtape", "#SELFIE", "the rain", "footsteps on the roof", "you breathe"]]

# bot
bot = commands.Bot(command_prefix="!")