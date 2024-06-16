import disnake as discord
from disnake.ext import commands

from main import Colors

import random

import requests


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Command that sends {endpoint}
        @bot.slash_command(name="send_animal", description="Sends animal on your choice in chat", options=[discord.Option(name="animal", type=discord.OptionType.string, description="Your animal", required=True, choices=[
            discord.OptionChoice(name="Dog", value="dog"),
            discord.OptionChoice(name="Cat", value="cat"),
            discord.OptionChoice(name="Fox", value="fox")
        ])])
        async def send_animal(self, ctx, animal: str):
            try:
                response = requests.get(f"https://some-random-api.com/animal/{animal}")
                data = response.json()

                if response.status_code == 200:
                    image = data["image"]
                    fact = data["fact"]

                    embed = discord.Embed(title=f"post this {animal} as fast as possible", description=f"``{fact}``", color=Colors.standard)
                    embed.set_image(url=image)

                elif response.status_code >= 400:
                    err = data["err"]

                    embed = discord.Embed(title=f"Something went wrong", description=f"``{response.status_code}`` | ``{err}``", color=Colors.standard)

                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.standard),
                               ephemeral=True)


        # Oracle (not Java vendor)
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
                embed = discord.Embed(title="Oracle", color=Colors.standard)
                embed.add_field(name=f"``{question}``", value=f"**{random.choice(random.choice(answers))}**")

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.standard),
                               ephemeral=True)
                

        # Famous game of rock, paper and scissors
        @bot.slash_command(name="rock_paper_scissors", description="Famous game of rock, paper and scissors", options=[discord.Option(name="choice", type=discord.OptionType.string, description="Your choice", required=True, choices=[
            discord.OptionChoice(name="Rock", value="rock"),
            discord.OptionChoice(name="Paper", value="paper"),
            discord.OptionChoice(name="Scissors", value="scissors")
        ])])
        async def ropasci(self, ctx, choice: str):
            try:
                embed = discord.Embed(title="Rock-Paper-Scissors", colors=Colors.standard)

                bot_choice = random.choice(["rock", "paper", "scissors"])
                result: str

                match (bot_choice, choice):
                    case ("rock", "scissors") | ("paper", "rock") | ("scissors", "paper"):
                        result = "bot won"

                    case ("scissors", "scissors") | ("rock", "rock") | ("paper", "paper"):
                        result = "draw"

                    case ("rock", "paper") | ("paper", "scissors") | ("scissors", "rock"):
                        result = "you won"

                    case _:
                        result = "what"

                embed.add_field(name=f"Your choice", value=f"``{choice}``")
                embed.add_field(name=f"Bot's choice", value=f"``{bot_choice}``")
                embed.add_field(name=f"Result", value=f"``{result}``")
                
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.standard),
                               ephemeral=True)
                

        # Random value
        @bot.slash_command(name="rand", description="Generate random number", options=[discord.Option(name="min", type=discord.OptionType.integer, description="Min value", required=True), discord.Option(name="max", type=discord.OptionType.integer, description="Max value", required=True)])
        async def rand(self, ctx, min: int, max: int):
            try:
                randvalue = random.randint(min, max)

                embed = discord.Embed(title="Random value", description=f"# ``{randvalue}``", color=Colors.standard)

                embed.add_field(name="Min value", value=f"``{min}``")
                embed.add_field(name="Max value", value=f"``{max}``")

                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.standard),
                               ephemeral=True)
                

def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
