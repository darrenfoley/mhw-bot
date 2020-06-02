import discord
from discord.ext import commands
from mhw_db import Monster

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


    @self._client.command(name='weak')
    @commands.is_owner()
    async def _weak(ctx, *, monster_name):
      monster = Monster(monster_name)
      weaknesses = monster.weaknesses()

      if len(weaknesses) == 0:
        await ctx.send(f'could not find weaknesses for {monster.name}')
      else:
        first = True
        str_weaknesses = f'{monster.name}:\n'
        star = '\\*'
        for w in weaknesses:
          str = f'  {w["element"]}: {star * w["stars"]}'
          if w['condition'] is not None:
            str += f' ({w["condition"]})'
          if not first:
            str_weaknesses += '\n'
          else:
            first = False
          str_weaknesses += str

        await ctx.send(str_weaknesses)
