import disnake as discord
from disnake.ext import commands

import requests as rq


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @bot.slash_command(name="send_cat", description="Посылает котика в чат")
        async def send_cat(self, ctx):
            try:
                response = rq.get("https://some-random-api.com/animal/cat").json()

                print(response)

                image = response["image"]
                fact = response["fact"]

                embed = discord.Embed(title="post this cat as fast as possible", description=fact, color=0xff0000)
                embed.set_image(url=image)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Что-то пошло не так", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
