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
                for m in monsters[:3]:
                    light_blue = 0x0091ff
                    embed = discord.Embed(title=m["name"], color=light_blue)

                    for r in m['resistances']:
                        if r['condition'] is not None:
                            condition_str = f' ({r["condition"]})'
                        else:
                            condition_str = ''
                        embed.add_field(name=r['element'], value='❌' + condition_str, inline=False)

                    for w in m['weaknesses']:
                        if w['condition'] is not None:
                            condition_str = f' ({w["condition"]})'
                        else:
                            condition_str = ''
                        embed.add_field(name=w['element'], value=('⭐' * w['stars']) + condition_str, inline=False)

                    await ctx.send(embed=embed)



def setup(client):
    client.add_cog(MHW(client))
