import discord
from discord.ext import commands
from mhw_db.mhw_db import Monster


class MHW(commands.Cog):

  def __init__(self, client):

    self._client = client



  @commands.command(name='weak')
  @commands.has_role('mhwtest')
  async def _weak(self, ctx, *, monster_name):

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




def setup(client):
  client.add_cog(MHW(client))
