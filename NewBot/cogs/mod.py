import disnake as discord
from disnake.ext import commands

import datetime

class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @commands.slash_command(name="kick",
                                description="Выгоняет выбранного пользователя с сервера",
                                options=[discord.Option(name="target",
                                                        type=discord.OptionType.user,
                                                        description="Пользователь для кика",
                                                        required=True),
                                         discord.Option(name="reason",
                                                        type=discord.OptionType.string,
                                                        description="Причина для кика",
                                                        required=False)])
        async def kick(self,
                       ctx,
                       target: discord.Member,
                       reason: str):
            if not ctx.author.guild_permissions.kick_members:
                await ctx.send(embed=discord.Embed(title="У вас недостаточно прав для этого!", color=0xff0000),
                               ephemeral=True)
                return

            if target.guild_permissions.kick_members:
                await ctx.send(embed=discord.Embed(title="Вы не можете выгнать модератора!", color=0xff0000),
                               ephemeral=True)
                return

            if target == ctx.author:
                await ctx.send(embed=discord.Embed(title="Вы не можете выгнать самого себя!", color=0xff0000),
                               ephemeral=True)
                return

            try:
                await target.kick(reason=reason)

                await ctx.send(
                    embed=discord.Embed(title=f"{target.display_name} изгнан по причине ``{reason}``", color=0xffbb00))

                print(f"{target.display_name} был изгнан")

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Что-то пошло не так", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)

        @commands.slash_command(name="mute",
                                description="Запрещает выбранному пользователю писать на сервере",
                                options=[discord.Option(name="target",
                                                        type=discord.OptionType.user,
                                                        description="Пользователь для мута",
                                                        required=True),
                                         discord.Option(name="days",
                                                        type=discord.OptionType.integer,
                                                        description="Кол-во дней мута",
                                                        required=False,
                                                        max_value=27),
                                         discord.Option(name="hours",
                                                        type=discord.OptionType.integer,
                                                        description="Кол-во часов мута",
                                                        required=False),
                                         discord.Option(name="minutes",
                                                        type=discord.OptionType.integer,
                                                        description="Кол-во минут мута",
                                                        required=False),
                                         discord.Option(name="seconds",
                                                        type=discord.OptionType.integer,
                                                        description="Кол-во секунд мута",
                                                        required=True),
                                         discord.Option(name="reason",
                                                        type=discord.OptionType.string,
                                                        description="Причина для мута",
                                                        required=False)])
        async def mute(self,
                       ctx,
                       target: discord.Member,
                       days: int = 0,
                       hours: int = 0,
                       minutes: int = 0,
                       seconds: int = 1,
                       reason: str = None):
            if not ctx.author.guild_permissions.mute_members:
                await ctx.send(embed=discord.Embed(title="У вас недостаточно прав для этого!", color=0xff0000),
                               ephemeral=True)
                return

            if target.guild_permissions.moderate_members:
                await ctx.send(embed=discord.Embed(title="Вы не можете замутить модератора!", color=0xff0000),
                               ephemeral=True)
                return

            if target == ctx.author:
                await ctx.send(embed=discord.Embed(title="Вы не можете замутить самого себя!", color=0xff0000),
                               ephemeral=True)
                return

            try:
                duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)

                await target.timeout(duration=duration, reason=reason)

                await ctx.send(embed=discord.Embed(
                    title=f"{target.display_name} замьючен на {days} дней, {hours} часов, {minutes} минут и {seconds} секунд",
                    color=0xffbb00))

                print(f"{target.display_name} замьючен на {days}d:{hours}h:{minutes}m:{seconds}s")

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Что-то пошло не так", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Mod(bot))
