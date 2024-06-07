# This cog is optional

import disnake as discord
from disnake.ext import commands

import openai
from json import load

with open(u"./non scripts/config.json", "r") as file:
    config = load(file)


class GPT(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        openai.api_key = config["OpenAI_Key"]


        # Func to get response from GPT
        def get_ai_response(ai_prompt: str):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": f"Your name is {bot.user.display_name} and you are a bot that helps"}, # Change this string for your needs
                    {"role": "user", "content": ai_prompt}
                ],
                n=1,
                max_tokens=999,
                temperature=.7
            )

            return str(response.choices[0].message.content)


        @bot.slash_command(name="ai", description="ChatGPT",
                           options=[
                               discord.Option(name="prompt",
                                              type=discord.OptionType.string,
                                              description="Your prompt",
                                              required=True)
                           ])
        async def ai(self, ctx, prompt: str):
            response = get_ai_response(prompt)

            try:
                await ctx.send(embed=discord.Embed(title="ChatGPT thinking...", color=0xffbb00))

                if len(response) <= 2000:
                    await ctx.edit_original_response(embed=discord.Embed(description=response, color=0xffbb00))

                else:
                    with open(u"../non scripts/gpt_answer_if_bigger_than_2k_chars.txt", "r") as file:
                        file.write(response)

                    await ctx.edit_original_response(embed=discord.Embed(title=f"Response's text was longer than Discord limits ({len(response)}/2000), so I send it as a file", color=0xffbb00), file=file)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(GPT(bot))