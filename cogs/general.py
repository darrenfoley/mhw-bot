import discord
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, client):
        self._client = client

    @commands.command(name="activity")
    @commands.is_owner()
    async def _activity(self, ctx, *, activity_name):
        activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
        await self._client.change_presence(activity=activity)


def setup(client):
    client.add_cog(General(client))
