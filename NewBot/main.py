import disnake as discord
from disnake.ext import commands
from json import load

path = "not-scripts/config.json"

with open(path, "r") as file:
    config = load(file)

intents = discord.Intents.all()

class Bot(commands.InteractionBot):
    def __init__(self):
        super().__init__(intents=intents)

        self.load_extension("cogs.mod")
        self.load_extension("cogs.utility")
        self.load_extension("cogs.fun")


if __name__ == "__main__":
    bot = Bot()

    @bot.event
    async def on_ready():
        print(f"{bot.user.display_name} ready to work")

    bot.run(config["Token"])
