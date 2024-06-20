import disnake as discord
from disnake.ext import commands

from main import Colors

from psutil import cpu_percent, virtual_memory

import ast
import math


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Server info command
        @bot.slash_command(name="server_info", description="Main info about current server")
        async def server_info(self, ctx):
            try:
                server = ctx.guild

                embed = discord.Embed(title=f"``{server.name}``", color=Colors.standard)

                embed.set_thumbnail(url=server.icon.url)

                embed.add_field(name="Server's owner", value=f"``{server.owner.display_name}`` ({server.owner.mention})")
                embed.add_field(name="Server's internal description", value=f"``{server.description if server.description else 'Empty'}``")

                embed.add_field(name="User count", value=f"``{len(server.members)}``")
                embed.add_field(name="Channel count", value=f"``{len(server.channels)}``")

                embed.add_field(name="Server ID", value=f"``{server.id}``")
                embed.add_field(name="Date of creation", value=f"``{server.created_at.strftime('%Y-%m-%d %H:%M:%S')}``")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error), ephemeral=True)


        # User info command
        @bot.slash_command(name="user_info", description="Info about target user", options=[
            discord.Option(name="member", type=discord.OptionType.user, description="User (on current server; you if not specified)", required=False)])
        async def user_info(self, ctx, member: discord.Member = None):
            try:
                if member is None:
                    member = ctx.author

                role_names = [role.name for role in member.roles[1:]]

                embed = discord.Embed(title=f"``{member.display_name}``", color=Colors.standard)
                embed.set_thumbnail(member.avatar.url)

                embed.add_field(name="Nickname", value=f"``{member.name}`` ({member.mention})")
                embed.add_field(name="ID", value=f"``{member.id}``")

                embed.add_field(name="Status", value=f"``{member.status}``")
                embed.add_field(name="Text in custom status", value=f"``{member.activity.name if member.activity else 'Empty'}``")

                embed.add_field(name="Joined Discord", value=f"<t:{round(member.created_at.timestamp())}:R>")
                embed.add_field(name="Joined this server", value=f"<t:{round(member.joined_at.timestamp())}:R>")

                embed.add_field(name="Is bot", value=f"``{'Yes' if member.bot else 'No'}``")
                embed.add_field(name="Roles", value=f"``{len(role_names) if role_names else 'No roles'}`` (``{'``, ``'.join(role_names) if role_names else '@everyone'}``)")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error), ephemeral=True)


        # Bot info command
        @bot.slash_command(name="about", description="Main info about Sigma Bot")
        async def about(self, ctx):
            try:
                client = bot.user
                with open("../../current-version") as file:
                    version = file.read()

                embed = discord.Embed(title=f"``{client.display_name}``", description="Just a bot with standard features", color=Colors.standard)

                embed.set_thumbnail(url=client.avatar.url)

                embed.add_field(name="Repository", value="https://github.com/sionit1337/sigma-bot")
                embed.add_field(name="Bot ID", value=f"``{client.id}``")

                embed.add_field(name="Version", value=f"``{version}``")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error), ephemeral=True)


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
                embed.add_field(name="RAM", value=f"``{ram_percent}``% (``{ram_used}``/``{ram_total}`` Mb)")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error), ephemeral=True)


        # Math
        @bot.slash_command(name="math", description="Solve math expression", options=[
            discord.Option(name="expr", type=discord.OptionType.string, description="Expression", required=True)])
        async def math(self, ctx, expr: str):
            try:
                def solve(expr: str):
                    parsed_expression = ast.parse(expr, mode="eval")

                    allowed_names = {
                    'sin': math.sin,
                    'cos': math.cos,
                    'tan': math.tan,
                    'log': math.log,
                    'sqrt': math.sqrt,
                    **vars(math)
                    }

                    solved = eval(compile(parsed_expression, filename="", mode="eval"), {}, allowed_names)

                    return solved


                embed = discord.Embed(title="Math expression", description=f"# ``{solve(expr)}``", color=Colors.standard)

                embed.add_field(name="Expression", value=f"``{expr}``")

                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.standard), ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
