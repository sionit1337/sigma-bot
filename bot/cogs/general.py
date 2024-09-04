import disnake as discord
from disnake.ext import commands

from main import (err_embed, here, Colors)
from json import load

from psutil import cpu_percent, virtual_memory
from random import randint


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


        # Bot info command
        @bot.slash_command(name="about", description="Main info about Sigma Bot")
        async def about(self, ctx):
            try:
                client = bot.user
                with open(f"{here}/not-scripts/config.json") as file:
                    version = load(file)["Version"]

                embed = discord.Embed(title=f"{client.display_name}", description="Just a bot with standard features", color=Colors.standard)

                embed.set_thumbnail(url=client.avatar.url)

                embed.add_field(name="Repository", value="https://github.com/sionit1337/sigma-bot")
                embed.add_field(name="Bot ID", value=f"``{client.id}``")

                embed.add_field(name="Version", value=f"``{version}``")

                await ctx.send(embed=embed)

            except Exception as e:
                await err_embed(ctx, e)


        # Host info command
        @bot.slash_command(name="host", description="Sends an info about bot's host (RAM load, ping, CPU load)")
        async def host(self, ctx):
            try:
                cpu = cpu_percent()

                ram_percent = virtual_memory().percent
                
                # 1 megabyte is 1048576 bytes y'know
                ram_used = round(virtual_memory().used / 1048576)
                ram_total = round(virtual_memory().total / 1048576)

                ping = round(bot.latency * 1000)

                embed = discord.Embed(title="Host stats", color=Colors.standard)

                embed.add_field(name="Ping", value=f"``{ping}ms``")
                embed.add_field(name="CPU", value=f"``{cpu}%``")
                embed.add_field(name="RAM", value=f"``{ram_percent}%`` (``{ram_used}Mb/{ram_total}Mb``)")

                await ctx.send(embed=embed)

            except Exception as e:
                await err_embed(ctx, e)


        # Echo
        @bot.slash_command(name="echo", description="Send message from bot's name (supports newlines)", options=[
            discord.Option(name="text", type=discord.OptionType.string, description="Text for sending", required=True)])
        async def echo(self, ctx, text: str):
            try:
                text = text.replace("\\n", "\n").replace("@everyone", "[everyone]").replace("@here", "[here]")

                await ctx.channel.send(text)
                
            except Exception as e:
                await err_embed(ctx, e)
                
                
        # Random value
        @bot.slash_command(name="rand", description="Generate random number", options=[
            discord.Option(name="min", type=discord.OptionType.integer, description="Min value", required=True), 
            discord.Option(name="max", type=discord.OptionType.integer, description="Max value", required=True)])
        async def rand(self, ctx, min: int, max: int):
            try:
                randvalue = randint(min, max)

                embed = discord.Embed(description=f"# ``{randvalue}``", color=Colors.standard)

                embed.add_field(name="Min value", value=f"``{min}``")
                embed.add_field(name="Max value", value=f"``{max}``")

                await ctx.send(embed=embed)
                
            except Exception as e:
                await err_embed(ctx, e)


def setup(bot: commands.Bot):
    bot.add_cog(General(bot))
