import disnake as discord
from disnake.ext import commands

from main import (Colors, err_embed)

from numexpr import evaluate

import gtts
import os


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Server info command
        @bot.slash_command(name="server_info", description="Main info about current server")
        async def server_info(self, ctx):
            try:
                server = ctx.guild
                role_names = [role.name for role in server.roles[1:]]

                embed = discord.Embed(title=f"{server.name}", color=Colors.standard)

                embed.set_thumbnail(url=server.icon.url)

                embed.add_field(name="Server's owner", value=f"``{server.owner.display_name}`` ({server.owner.mention})")
                embed.add_field(name="Server's internal description", value=f"``{server.description if server.description else 'Empty'}``")

                embed.add_field(name="User count", value=f"``{len(server.members)}``")
                embed.add_field(name="Channel count", value=f"``{len(server.channels)}``")

                embed.add_field(name="Server ID", value=f"``{server.id}``")
                embed.add_field(name="Date of creation", value=f"<t:{server.created_at.timestamp()}:>")

                embed.add_field(name="Roles count", value=f"``{len(role_names) if role_names else 'No roles'}`` (``{'``, ``'.join(role_names) if role_names else '@everyone'}``)")

                await ctx.send(embed=embed)

            except Exception as e:
                await err_embed(ctx, e)


        # User info command
        @bot.slash_command(name="user_info", description="Info about target user", options=[
            discord.Option(name="member", type=discord.OptionType.user, description="User (on current server; you if not specified)", required=False)])
        async def user_info(self, ctx, member: discord.Member = None):
            try:
                if member is None:
                    member = ctx.author

                role_names = [role.name for role in member.roles[1:]]
                status_name = {
                    "online": "Online",
                    "dnd": "Don't Disturb",
                    "do_not_disturb": "Don't Disturb",
                    "idle": "Idling",
                    "offline": "Offline",
                    "invisible": "Unknown (invisible)",
                    "streaming": "Streaming something"
                }

                embed = discord.Embed(title=f"{member.display_name}", color=Colors.standard)
                embed.set_thumbnail(member.avatar.url)

                embed.add_field(name="Name identifier", value=f"``{member.name}`` ({member.mention})")
                embed.add_field(name="ID", value=f"``{member.id}``")

                embed.add_field(name="Status", value=f"``{status_name[str(member.status)]}``")

                embed.add_field(name="Joined Discord", value=f"<t:{round(member.created_at.timestamp())}:>")
                embed.add_field(name="Joined this server", value=f"<t:{round(member.joined_at.timestamp())}:>")

                embed.add_field(name="Is bot", value=f"``{'Yes' if member.bot else 'No'}``")
                
                embed.add_field(name="Roles", value=f"``{len(role_names) if role_names else 'No roles'}`` (``{'``, ``'.join(role_names) if role_names else '@everyone'}``)")

                await ctx.send(embed=embed)

            except Exception as e:
                await err_embed(ctx, e)


        # Math
        @bot.slash_command(name="math", description="Solve math expression", options=[
            discord.Option(name="expr", type=discord.OptionType.string, description="Expression", required=True)])
        async def math(self, ctx, expr: str):
            try:
                def solve(expr: str):
                    try:
                        solved = evaluate(expr)
                        return solved
                    
                    except Exception:
                        return "Expression couldn't be solved"


                embed = discord.Embed(description=f"# ``{solve(expr)}``", color=Colors.standard)

                embed.add_field(name="Expression", value=f"``{expr}``")

                await ctx.send(embed=embed)
                
            except Exception as e:
                await err_embed(ctx, e)


        # TTS
        @bot.slash_command(name="tts", description="Text to Speech", options=[
            discord.Option(name="text", type=discord.OptionType.string, description="Text", required=True),
            discord.Option(name="lang", type=discord.OptionType.string, description="Language", required=True, choices=[
            discord.OptionChoice(name="Russian", value="ru"),
            discord.OptionChoice(name="English", value="en"),
            discord.OptionChoice(name="Spanish", value="es"),
            discord.OptionChoice(name="Portuguese", value="pt"),
            discord.OptionChoice(name="French", value="fr"),
            discord.OptionChoice(name="Chinese (traditional)", value="zh-TW"),
            discord.OptionChoice(name="Chinese (simplified)", value="zh-CN"),
            ])])
        async def tts(self, ctx, text: str, lang: str):
            try:
                voice = gtts.gTTS(text, lang=lang)
                voice.save(f"{os.path.realpath(os.path.dirname(__file__))}/temp/voice.ogg")
                await ctx.send(embed=discord.Embed(description=f"``{text}``", color=Colors.standard), file=discord.File(f"{os.path.realpath(os.path.dirname(__file__))}/temp/voice.ogg"))
                
            except Exception as e:
                await err_embed(ctx, e)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
