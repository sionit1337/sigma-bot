import disnake as discord
from disnake.ext import commands
from json import load

with open(u"./non scripts/config.json", "r") as file:
    config = load(file)

intents = discord.Intents.all()

class Bot(commands.InteractionBot):
    def __init__(self):
        super().__init__(intents=intents)

        self.load_extension("cogs.mod")


if __name__ == "__main__":
    bot = Bot()

    @bot.event
    async def on_ready():
        print(f"{bot.user.display_name} готов к работе")


    bot.run(config["Token"])
