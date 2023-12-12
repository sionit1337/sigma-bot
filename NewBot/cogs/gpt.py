import disnake as discord
from disnake.ext import commands

import openai
from json import load

with open(u"./non scripts/config.json", "r") as file:
    config = load(file)


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        openai.api_key = config["OpenAI_Key"]

        def get_ai_response(ai_prompt: str):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Ты Sigma Bot, был создан sionit_1337. Ты находишься на дискорд-сервере 『Σ』Syndicate Sigma и общаешься исключительно на русском"},
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
                                              description="Ваш вопрос",
                                              required=True)
                           ])
        async def ai(self, ctx, prompt: str):
            response = get_ai_response(prompt)

            try:
                await ctx.send(embed=discord.Embed(title="ChatGPT думает...", color=0xffbb00))

                if len(response) <= 2000:
                    await ctx.edit_original_response(embed=discord.Embed(description=response, color=0xffbb00))

                else:
                    with open(u"../non scripts/gpt_answer_if_bigger_than_2k_chars.txt", "r") as file:
                        file.write(response)

                    await ctx.edit_original_response(embed=discord.Embed(title=f"Текст ответа был больше лимита дискорда ({len(response)}/2000), поэтому я отправил его в виде файла", color=0xffbb00), file=file)

            except Exception as e:
                await ctx.send(embed=discord.Embed(title="Что-то пошло не так", description=f"``{e}``", color=0xff0000),
                               ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))