import disnake as discord
from disnake.ext import commands

import random

import requests


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Command that sends cat
        @bot.slash_command(name="send_cat", description="Sends cat in chat")
        async def send_cat(self, ctx):
            try:
                response = requests.get("https://some-random-api.com/animal/cat")
                data = response.json()

                image = data["image"]
                fact = data["fact"]

                embed = discord.Embed(title="post this cat as fast as possible", description=f"Fact: ``{fact}`` \n(it's embedded in API y'know)", color=0xffbb00)
                embed.set_image(url=image)

                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


        # I think everyone knows this command
        @bot.slash_command(name="ball8", description="Asks oracle and answers your questions",
                           options=[discord.Option(name="question", type=discord.OptionType.string, description="Your question", required=True)
                           ])
        async def ball8(self, ctx, question: str):
            answers_positive = ["Definitely yes", "It is certain", "You can rely on it"]
            answers_negative = ["Very doubtful", "My reply is no", "Don't count on it"]
            answers_questionable = ["Sources say yes", "Yes", "Outlook good"]
            answers_neutral = ["Reply hazy, try again", "Cannot predict now", "Concetrate and ask again"]

            answers = [answers_positive, answers_negative, answers_questionable, answers_neutral]

            try:
                embed = discord.Embed(title="Oracle", color=0xffbb00)
                embed.add_field(name=f"``{question}``", value=f"**{random.choice(random.choice(answers))}**")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
