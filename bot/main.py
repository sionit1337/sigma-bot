import disnake as discord
from disnake.ext import commands
from json import load

import os

from random import choice

from logger import Logger
import logging


here = os.path.realpath(os.path.dirname(__file__))

logger = Logger(here, "bot")
logger.init_logger()


class Colors:
    standard = 0xff9900
    error = 0xff0033


async def err_embed(ctx: commands.Context, e: Exception):
    await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"``{e}``", color=Colors.error),  ephemeral=True)
    logger.log(e, logging.ERROR)


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
                self.logger.log(f"Successfully loaded cog \"{cog}\"", logging.INFO)

            except Exception as e:
                self.logger.log(e, logging.ERROR)


if __name__ == "__main__":
    bot = Bot()

    @bot.event
    async def on_ready():
        bot.logger.log(f"Logged in as {bot.user.display_name}", logging.INFO)
        bot.setup_cogs()
        
        motds = [
            "Visual Studio Code", 
            "with the /echo", 
            "no /help command, sorry"
            ]
        motd = discord.Game(choice(motds))
        await bot.change_presence(status=discord.Status.online, activity=motd)

    bot.run(bot.get_config["Token"])
