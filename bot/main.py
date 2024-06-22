import disnake as discord
from disnake.ext import commands
from json import load

import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="logs/bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


# Universal colors
class Colors:
    standard = 0xff9900
    error = 0xff0000
    todo = 0x5500ff


async def err_embed(ctx, e):
    await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"{e}", color=Colors.error), ephemeral=True)


cfg_path = "bot/not-scripts/config.json"

with open(cfg_path, "r") as file:
    config = load(file)

intents = discord.Intents.all()

class Bot(commands.InteractionBot):
    def __init__(self):
        super().__init__(intents=intents)

    def setup_interactions(self):
        self.load_extension("cogs.mod")
        self.load_extension("cogs.utility")
        self.load_extension("cogs.fun")


if __name__ == "__main__":
    bot = Bot()

    @bot.event
    async def on_ready():
        print(f"{bot.user.display_name} is ready to work")

    bot.setup_interactions()
    bot.run(config["Token"])
