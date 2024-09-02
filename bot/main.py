import disnake as discord
from disnake.ext import commands
from json import load

import os

from random import choice

import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s] (%(levelname)s) %(name)s: %(message)s")
here = os.path.realpath(os.path.dirname(__file__))

file_handler = logging.FileHandler(filename=f"{here}/logs/bot.log", encoding="utf-8", mode="w")
console_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Universal colors
class Colors:
    standard = 0xff9900
    error = 0xff0033


async def err_embed(ctx, e):
    await ctx.send(
        embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error), 
        ephemeral=True
        )
    logger.error(e)


cfg_path = f"{here}/not-scripts/config.json"

with open(cfg_path, "r") as file:
    config = load(file)

intents = discord.Intents.all()

class Bot(commands.InteractionBot):
    def __init__(self):
        self._config = config
        self.logger = logger
        super().__init__(intents=intents)
        
        
        @property
        def get_config(self):
            return self._config


    def setup_cogs(self):
        for file in os.listdir(f"{here}/cogs"):
            if not file.endswith(".py"):
                continue
            
            cog = file[:-3] # Looks like :3 lol

            try:
                self.load_extension(f"cogs.{cog}")
                self.logger.info(f"Successfully loaded cog \"{cog}\"")

            except Exception as e:
                self.logger.error(e)


if __name__ == "__main__":
    bot = Bot()

    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user.display_name}")
        bot.setup_cogs()
        
        motds = [
            "Visual Studio Code", 
            "with the /echo", 
            "no /help command, sorry"
            ]
        motd = discord.Game(choice(motds))
        await bot.change_presence(status=discord.Status.online, activity=motd)

    bot.run(bot.get_config["Token"])
