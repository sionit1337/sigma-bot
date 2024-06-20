# This cog is optional

import disnake as discord
from disnake.ext import commands

from main import (Colors, blacklist)

import openai
from json import load
import craiyon
from random import choice

with open(u"./non scripts/config.json", "r") as file:
    config = load(file)


class AITools(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        openai.api_key = config["OpenAI_Key"]


        # Func to get response from GPT
        def get_ai_response(ai_prompt: str):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": f"Your name is {bot.user.display_name} and you are a bot that helps"}, # Change for your needs
                    {"role": "user", "content": ai_prompt}
                ],
                n=1,
                max_tokens=500,
                temperature=.7 # Change for your needs
            )

            return str(response.choices[0].message.content)


        # Command to talk with ChatGPT
        @bot.slash_command(name="gpt", description="Ask ChatGPT", options=[
            discord.Option(name="prompt", type=discord.OptionType.string, description="Your prompt", required=True)])
        async def ai(self, ctx, prompt: str):
            try:
                response = get_ai_response(prompt)

                await ctx.send(embed=discord.Embed(title="ChatGPT thinking...", color=Colors.standard))

                if len(response) <= 2000:
                    await ctx.edit_original_response(embed=discord.Embed(description=response, color=Colors.standard))

                else:
                    with open("../not-scripts/response.txt", "w") as file:
                        file.write(response)

                        await ctx.edit_original_response(embed=discord.Embed(title=f"Response's text was longer than Discord limits ({len(response)}/2000), so I send it as a file", color=Colors.standard), file=file)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error), ephemeral=True)
                

        # Command to generate images
        @bot.slash_command(name="imagine", description="Generate image with Craiyon", options=[
            discord.Option(name="prompt", type=discord.OptionType.string, description="Your prompt", required=True)])
        async def imagine(self, ctx, prompt: str):
            try:
                generator = craiyon.Craiyon()

                embed = discord.Embed(title="Generating...", color=Colors.standard)
                await ctx.send(embed=embed)

                generated = await generator.async_generate(prompt)

                embed = discord.Embed(title=f"``{prompt}``", color=Colors.standard)
                embed.set_image(url=choice(generated.images))

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error), ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(AITools(bot))