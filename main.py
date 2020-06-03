import json
from bot import Bot
from discord.ext import commands


with open('./config.json') as f:
  config = json.load(f)

bot = Bot(config)
bot.run()
