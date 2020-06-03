import discord
from discord.ext import commands
from mhw_db.mhw_db import Monster


class MHW(commands.Cog):

  def __init__(self, client):

    self._client = client



  @commands.command(name='weak')
  async def _weak(self, ctx, *, monster_name):

    async with ctx.channel.typing():

      monster = Monster(monster_name)
      monsters = await monster.weaknesses()
      if len(monsters) == 0:
        await ctx.send(f'could not find weaknesses for {monster.name}')
      else:
        star = '\\*'
        message = 'I found this...'
        first_monster = True
        for m in monsters:
          if not first_monster:
            message += '\n\n'
          else:
            first_monster = False
          message += f'\n**{m["name"]}:**\n'
          for w in m['weaknesses']:
            weakness_str = f'\n  {w["element"]}: {star * w["stars"]}'
            if w['condition'] is not None:
              weakness_str += f' ({w["condition"]})'
            message += weakness_str

        await ctx.send(message)




def setup(client):
  client.add_cog(MHW(client))
