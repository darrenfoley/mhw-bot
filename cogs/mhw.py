import json
import os

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

    @commands.command(name='quest')
    async def _quest(self, ctx, *, quest_name):
        path = './data/quests.json'

        if not os.path.exists(path):
            await ctx.send('something went wrong')
            print(f'path [{path}] does not exist')
            return

        # can i open file async?
        with open(path, 'r') as f:
            quests = json.load(f)

        filtered_quests = {key: value for key, value in quests.items() if quest_name.lower() in key.lower()}

        if len(filtered_quests) == 0:
            await ctx.send(f'I couldn\'t find any quests for "{quest_name}"')
            return

        for key, value in filtered_quests.items():
            light_blue = 0x0091ff
            embed = discord.Embed(title=key, url=value['link'], colour=light_blue)
            if value['category'] is not None:
                description = value['category'][:-1] if value['category'].endswith('s') else value['category']
                embed.description = description
            if value['quote'] is not None:
                embed.add_field(name='Description', value=value['quote'], inline=False)
            if value['info'] is not None:
                for info_key, info_values in value['info'].items():
                    # TODO: is there a better way to sanitize crap out of these?
                    v = ''.join(info_values)
                    if len(v.strip()) != 0:
                        embed.add_field(name=info_key, value=v, inline=False)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(MHW(client))
