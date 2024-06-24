import disnake as discord
from disnake.ext import commands
from json import load

from random import choice

import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

file_handler = logging.FileHandler(filename="../logs/launcher.log", encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Universal colors
class Colors:
    standard = 0xff9900
    error = 0xff0000
    todo = 0x5500ff


async def err_embed(ctx, e):
    await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"{e}", color=Colors.error), ephemeral=True)
    logger.error(e)


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
        self.load_extension("cogs.general")


if __name__ == "__main__":
    bot = Bot()

    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user.display_name}")

    bot.setup_interactions()
    bot.run(config["Token"])
