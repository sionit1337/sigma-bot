import disnake as discord
from disnake.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @bot.slash_command(name="info", description="Информация о сервере на котором вы находитесь")
        async def info(self, ctx):
            server = ctx.guild

            try:
                embed = discord.Embed(title=f"``{server.name}``", color=0xffbb00)

                embed.set_thumbnail(url=server.icon.url)

                embed.add_field(name="Владелец сервера", value=f"``{server.owner.display_name}`` ({server.owner.mention})")
                embed.add_field(name="Описание сервера", value=f"``{server.description}``")

                embed.add_field(name="Количество участников", value=f"``{len(server.members)}``")
                embed.add_field(name="Количество каналов", value=f"``{len(server.channels)}``")

                embed.add_field(name="ID сервера", value=f"``{server.id}``")
                embed.add_field(name="Дата создания", value=f"``{server.created_at.strftime('%Y-%m-%d %H:%M:%S')}``")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Что-то пошло не так", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))