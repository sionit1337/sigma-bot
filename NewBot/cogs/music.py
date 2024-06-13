# TODO

import disnake as discord
from disnake.ext import commands

from main import Colors

import yt_dlp as ytdl
from json import load

with open(u"./non scripts/config.json", "r") as file:
    config = load(file)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


        @bot.slash_command(name="play", description="Play music")
        async def play(self, ctx):
            try:
                await ctx.send(embed=discord.Embed(title="TODO", color=Colors.todo))

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error),
                               ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))