import disnake as discord
from disnake.ext import commands

from main import (Colors, err_embed)

import datetime


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Kick command
        @bot.slash_command(name="kick", description="Kicks selected user from server", options=[
            discord.Option(name="target", type=discord.OptionType.user, description="Target user", required=True), 
            discord.Option(name="reason", type=discord.OptionType.string, description="Reason for kick", required=False)])
        async def kick(self, ctx, target: discord.Member, reason: str):
            if not ctx.author.guild_permissions.kick_members:
                await err_embed(ctx, "Not enough permissions!")
                return

            if target.guild_permissions.kick_members:
                await err_embed(ctx, "You can't kick another moderator!")
                return

            if target == ctx.author or target == bot.user:
                await err_embed(ctx, "You can't kick yourself or bot!")
                return

            try:
                await target.kick(reason=reason)

                embed = discord.Embed(title="Kicked", color=Colors.standard)

                embed.add_field(name="Moderator", value=f"``{ctx.author.display_name}``")
                embed.add_field(name="Target", value=f"``{target.display_name}``")

                embed.add_field(name="Reason", value=f"``{reason if reason else 'Reason wasn\'t specified'}``")

                await ctx.send(embed=embed)

                await ctx.delete_original_response(delay=10)

            except Exception as e:
                await err_embed(ctx, e)


        # Mute command
        @bot.slash_command(name="mute", description="Disallow target user's ability to speak", options=[
            discord.Option(name="target", type=discord.OptionType.user, description="Target user for mute", required=True),
            discord.Option(name="time", type=discord.OptionType.integer, description="Time for mute in seconds (e.g. typed \"3600\" - mutes for 1 hour)", required=False),
            discord.Option(name="reason", type=discord.OptionType.string, description="Reason for mute", required=False)])
        async def mute(self, ctx, target: discord.Member, time: int = 60, reason: str = None):
            if not ctx.author.guild_permissions.moderate_members:
                await err_embed(ctx, "Not enough permissions!")
                return

            if target.guild_permissions.moderate_members:
                await err_embed(ctx, "You can't mute another moderator!")
                return

            if target == ctx.author or target == bot.user:
                await err_embed(ctx, "You can't mute yourself or bot!")
                return

            try:
                time = min(2419200, time) # limits time for 2 weeks

                duration = datetime.timedelta(0, time)

                await target.timeout(duration=duration, reason=reason)

                embed = discord.Embed(title="Muted", color=Colors.standard)

                embed.add_field(name="Moderator", value=f"``{ctx.author.display_name}``")
                embed.add_field(name="Target", value=f"``{target.display_name}`` ({target.mention})")

                embed.add_field(name="Time", value=f"``{time}secs``")
                embed.add_field(name="Reason", value=f"``{reason if reason else 'Reason wasn\'t specified'}``")

                await ctx.send(embed=embed)

                await ctx.delete_original_response(delay=10)

            except Exception as e:
                await err_embed(ctx, e)


        # Ban command
        @bot.slash_command(name="ban", description="Kicks user AND disallows him to return", options=[
            discord.Option(name="target", type=discord.OptionType.user, description="Target user for ban", required=True),
            discord.Option(name="reason", type=discord.OptionType.string, description="Ban reason", required=False)])
        async def ban(self, ctx, target: discord.Member, reason: str):
            if not ctx.author.guild_permissions.kick_members:
                await err_embed(ctx, "Not enough permissions!")
                return

            if target.guild_permissions.kick_members:
                await err_embed(ctx, "You can't ban another moderator!")
                return

            if target == ctx.author or target == bot.user:
                await err_embed(ctx, "You can't ban yourself or bot!")
                return

            try:
                await target.ban(reason=reason, clean_history_duration=datetime.timedelta(days=30))

                embed = discord.Embed(title="Banned", color=Colors.standard)

                embed.add_field(name="Moderator", value=f"``{ctx.author.display_name}``")
                embed.add_field(name="Target", value=f"``{target.display_name}``")

                embed.add_field(name="Reason", value=f"``{reason if reason else 'Reason wasn\'t specified'}``")

                await ctx.send(embed=embed)

                await ctx.delete_original_response(delay=10)

            except Exception as e:
                await err_embed(ctx, e)


        @bot.slash_command(name="clear", description="Cleans chat from selected number of messages", options=[
            discord.Option(name="amount", type=discord.OptionType.integer, description="Target message count", required=True)])
        async def clear(self, ctx, amount: int):
            if not ctx.author.guild_permissions.manage_messages:
                await err_embed(ctx, "Not enough permissions!")
                return

            try:
                await ctx.channel.purge(limit=amount)

                embed = discord.Embed(title="Cleared messages", color=Colors.standard)

                embed.add_field(name="Moderator", value=f"``{ctx.author.display_name}``")

                embed.add_field(name="Amount", value=f"``{amount}msgs``")

                await ctx.send(embed=embed)

                await ctx.delete_original_response(delay=10)

            except Exception as e:
                await err_embed(ctx, e)


def setup(bot: commands.Bot):
    bot.add_cog(Mod(bot))
