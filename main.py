import json

from bot import Bot

with open('./config.json') as f:
    config = json.load(f)

bot = Bot(config)
bot.run()
