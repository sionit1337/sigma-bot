import disnake as discord
from disnake.ext import commands

from main import (Colors, err_embed, logger)
from json import load

from psutil import cpu_percent, virtual_memory


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logger


        # Bot info command
        @bot.slash_command(name="about", description="Main info about Sigma Bot")
        async def about(self, ctx):
            try:
                client = bot.user
                with open("bot/not-scripts/config.json") as file:
                    version = load(file)["Version"]

                embed = discord.Embed(title=f"{client.display_name}", description="Just a bot with standard features", color=Colors.standard)

                embed.set_thumbnail(url=client.avatar.url)

                embed.add_field(name="Repository", value="https://github.com/sionit1337/sigma-bot")
                embed.add_field(name="Bot ID", value=f"``{client.id}``")

                embed.add_field(name="Version", value=f"``{version}``")

                await ctx.send(embed=embed)

            except Exception as e:
                await err_embed(ctx, e)

            finally:
                self.logger.info(f"{ctx.author}: /about")


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

            finally:
                self.logger.info(f"{ctx.author}: /host")


        # Echo
        @bot.slash_command(name="echo", description="Send message from bot's name", options=[
            discord.Option(name="text", type=discord.OptionType.string, description="Text for sending", required=True)])
        async def echo(self, ctx, text: str):
            try:
                text = text.replace("@everyone", "[everyone]")
                text = text.replace("@here", "[here]")

                await ctx.channel.send(text)
                
            except Exception as e:
                await err_embed(ctx, e)

            finally:
                self.logger.info(f"{ctx.author}: /echo")


        # Eval
        @bot.slash_command(name="eval", description="RESTRICTED ACCESS", options=[
            discord.Option(name="code", type=discord.OptionType.string, description="Code you want to evaluate", required=True)])
        @bot.is_owner
        async def evalvlvl(self, ctx, text: str):
            try:
                text = text.replace("@everyone", "[everyone]")
                text = text.replace("@here", "[here]")

                await ctx.channel.send(text)
                
            except Exception as e:
                await err_embed(ctx, e)

            finally:
                self.logger.info(f"{ctx.author}: /eval")


def setup(bot: commands.Bot):
    bot.add_cog(General(bot))
