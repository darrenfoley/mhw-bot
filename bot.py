import discord
from discord.ext import commands

class MHW:

  def __init__(self, config):

    self._config = config
    self._client = commands.Bot(command_prefix=self._config['discord']['prefix'])
    self._register_events()
    self._register_commands()



  def run(self):

    self._client.run(self._config['discord']['token'])



  def _register_events(self):
    async def on_ready():
      print('Bot is ready')
    self._client.add_listener(on_ready)



  def _register_commands(self):

    @self._client.command(name='echo')
    @commands.is_owner()
    async def _echo(ctx, *, phrase):
      await ctx.send(phrase)
