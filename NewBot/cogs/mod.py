import disnake as discord
from disnake.ext import commands

import datetime
import re

class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Kick command
        @bot.slash_command(name="kick",
                           description="Kicks selected user from server",
                           options=[discord.Option(name="target", type=discord.OptionType.user, description="Target user", required=True),
                                    discord.Option(name="reason", type=discord.OptionType.string, description="Reason for kick", required=False)])
        async def kick(self,
                       ctx,
                       target: discord.Member,
                       reason: str):
            if not ctx.author.guild_permissions.kick_members:
                await ctx.send(embed=discord.Embed(title="Not enough permissions!", color=0xff0000),
                               ephemeral=True)
                return

            if target.guild_permissions.kick_members:
                await ctx.send(embed=discord.Embed(title="You can't kick another moderator!", color=0xff0000),
                               ephemeral=True)
                return

            if target == ctx.author:
                await ctx.send(embed=discord.Embed(title="You can't kick yourself!", color=0xff0000),
                               ephemeral=True)
                return

            try:
                await target.kick(reason=reason)

                await ctx.send(
                    embed=discord.Embed(title=f"``{target.display_name}`` was kicked for ``{reason}``", color=0xffbb00))

                print(f"{target.display_name} was kicked")

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


        # Mute command
        @bot.slash_command(name="mute",
                           description="Disallow target user's ability to speak",
                           options=[discord.Option(name="target", type=discord.OptionType.user, description="Target user for mute", required=True),
                                    discord.Option(name="time", type=discord.OptionType.integer, description="Time for mute in seconds (e.g. typed \"3600\" - mutes for 1 hour)", required=False),
                                    discord.Option(name="reason", type=discord.OptionType.string, description="Reason for mute", required=False)])
        async def mute(self,
                       ctx,
                       target: discord.Member,
                       time: int = 60,
                       reason: str = None):
            if not ctx.author.guild_permissions.mute_members:
                await ctx.send(embed=discord.Embed(title="Not enough permissions!", color=0xff0000),
                               ephemeral=True)
                return

            if target.guild_permissions.moderate_members:
                await ctx.send(embed=discord.Embed(title="You can't mute another moderator!", color=0xff0000),
                               ephemeral=True)
                return

            if target == ctx.author:
                await ctx.send(embed=discord.Embed(title="You can't mute yourself!", color=0xff0000),
                               ephemeral=True)
                return

            try:
                time = min(2419200, time) # limits time for 2 weeks

                duration = datetime.timedelta(0, time)

                await target.timeout(duration=duration, reason=reason)

                await ctx.send(embed=discord.Embed(
                    title=f"``{target.display_name}`` has been muted for ``{time}`` seconds and for reason: ``{reason}``",
                    color=0xffbb00))

                print(f"{target.display_name} was muted for {time}s")

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


        # Ban command
        @bot.slash_command(name="ban",
                           description="Kicks user AND disallows him to return",
                           options=[discord.Option(name="target", type=discord.OptionType.user, description="Target user for ban", required=True),
                                    discord.Option(name="reason", type=discord.OptionType.string, description="Ban reason", required=False)])
        async def ban(self,
                      ctx,
                      target: discord.Member,
                      reason: str):
            if not ctx.author.guild_permissions.kick_members:
                await ctx.send(embed=discord.Embed(title="Not enough permissions!", color=0xff0000),
                               ephemeral=True)
                return

            if target.guild_permissions.kick_members:
                await ctx.send(embed=discord.Embed(title="You can't ban another moderator!", color=0xff0000),
                               ephemeral=True)
                return

            if target == ctx.author:
                await ctx.send(embed=discord.Embed(title="You can't ban yourself!", color=0xff0000),
                               ephemeral=True)
                return

            try:
                await target.ban(reason=reason, clean_history_duration=datetime.timedelta(days=30))

                await ctx.send(
                    embed=discord.Embed(title=f"``{target.display_name}`` has been banned for ``{reason}``", color=0xffbb00))

                print(f"{target.display_name} has been banned")

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


        @bot.slash_command(name="clear",
                           description="Cleans chat from selected number of messages",
                           options=[discord.Option(name="amount", type=discord.OptionType.integer, description="Target message count", required=True)])
        async def ban(self,
                      ctx,
                      amount: int):
            if not ctx.author.guild_permissions.manage_messages:
                await ctx.send(embed=discord.Embed(title="Not enough permissions!", color=0xff0000),
                               ephemeral=True)
                return

            try:
                await ctx.channel.purge(limit=amount)

                await ctx.send(
                    embed=discord.Embed(title=f"``{amount}`` was cleared",
                                        color=0xffbb00))

                print(f"{amount} messages in #{ctx.channel} was gone")

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Mod(bot))
