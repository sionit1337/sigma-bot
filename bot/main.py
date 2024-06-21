import disnake as discord
from disnake.ext import commands
from json import load
import os


# Universal colors
class Colors:
    standard = 0xff9900
    error = 0xff0000
    todo = 0x5500ff


async def err_embed(ctx, e):
    await ctx.send(embed=discord.Embed(title="Something went wrong", description=f"{e}", color=Colors.error), ephemeral=True)


cfg_path = "./not-scripts/config.json"

with open(cfg_path, "r") as file:
    config = load(file)

intents = discord.Intents.all()

class Bot(commands.InteractionBot):
    def __init__(self):
        super().__init__(intents=intents)

    async def setup_interactions(self):
        await self.load_extension("cogs.mod")
        await self.load_extension("cogs.utility")
        await self.load_extension("cogs.fun")
        await self.load_extension("cogs.music")
        await self.load_extension("cogs.ai_tools")


if __name__ == "__main__":
    bot = Bot()

    @bot.event
    async def on_ready():
        print(f"{bot.user.display_name} ready to work")

    bot.setup_interactions()
    bot.run(config["Token"])
