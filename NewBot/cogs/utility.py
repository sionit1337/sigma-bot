import disnake as discord
from disnake.ext import commands

from psutil import cpu_percent, virtual_memory


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @bot.slash_command(name="server_info", description="Информация о сервере на котором вы находитесь")
        async def server_info(self, ctx):
            server = ctx.guild

            try:
                embed = discord.Embed(title=f"``{server.name}``", color=0xffbb00)

                embed.set_thumbnail(url=server.icon.url)

                embed.add_field(name="Владелец сервера", value=f"``{server.owner.display_name}`` ({server.owner.mention})")
                embed.add_field(name="Описание сервера", value=f"``{server.description if server.description else 'Пусто'}``")

                embed.add_field(name="Количество участников", value=f"``{len(server.members)}``")
                embed.add_field(name="Количество каналов", value=f"``{len(server.channels)}``")

                embed.add_field(name="ID сервера", value=f"``{server.id}``")
                embed.add_field(name="Дата создания", value=f"``{server.created_at.strftime('%Y-%m-%d %H:%M:%S')}``")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Что-то пошло не так", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)

        @bot.slash_command(name="user_info", description="Информация о выбранном пользователе",
                           options=[
                               discord.Option(name="member",
                                              type=discord.OptionType.user,
                                              description="Пользователь",
                                              required=False
                                              )
                           ]
                           )
        async def user_info(self, ctx, member: discord.Member = None):
            if member is None:
                member = ctx.author

            role_names = [role.name for role in member.roles[1:]]

            try:
                embed = discord.Embed(title=f"``{member.display_name}``")
                embed.set_thumbnail(member.avatar.url)

                embed.add_field(name="Ник", value=f"``{member.global_name}``")
                embed.add_field(name="Статус", value=f"``{member.status}``")
                embed.add_field(name="Бот", value=f"``{'Да' if member.bot else 'Нет'}``")
                embed.add_field(name="Текст в статусе", value=f"``{member.activity.name if member.activity else 'Пусто'}``")
                embed.add_field(name="Роли", value=f"``{len(role_names)}`` (``{'``, ``'.join(role_names)}``)")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Что-то пошло не так", description=f"``{e}``", color=0xff0000), ephemeral=True)


        @bot.slash_command(name="host", description="Пишет нагрузку на машину, хостящую бота")
        async def host(self, ctx):

            cpu = cpu_percent()

            ram_percent = virtual_memory().percent
            ram_used = round(virtual_memory().used / 1048576)
            ram_total = round(virtual_memory().total / 1048576)

            ping = round(bot.latency * 1000)

            try:
                embed = discord.Embed(title="Нагрузка на машину", color=0xffbb00)

                embed.add_field(name="Пинг", value=f"``{ping}`` мс")
                embed.add_field(name="Процессор", value=f"``{cpu}%``")
                embed.add_field(name="Оперативная память", value=f"``{ram_percent}``% (``{ram_used}``/``{ram_total}`` МБ)")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Что-то пошло не так", description=f"``{e}``", color=0xff0000), ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
