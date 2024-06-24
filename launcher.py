from json import load
import os
import re
import requests

import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

file_handler = logging.FileHandler(filename="logs/launcher.log", encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

cfg_path = "./bot/not-scripts/config.json"

with open(cfg_path, "r") as file:
    config = load(file)


class Launcher:
    def __init__(self):
        self.config = config
        self.logger = logger


    def check_config(self):
        self.logger.info("Checking config for token...")

        pattern = re.compile("[-a-zA-Z0-9_].[-a-zA-Z0-9_].[-a-zA-Z0-9_]")
        match = re.search(pattern, self.config["Token"])

        if not match:
            self.logger.warning("Token wasn't found")

            self.logger.info("Insert the token in config and restart laucher to apply the changes")
            return

        else:
            self.logger.info("Token was found")

            self.start_bot()


    def check_updates(self):
        self.logger.info("Checking for updates...")

        latest_config = requests.get("https://raw.githubusercontent.com/sionit1337/sigma-bot/main/bot/not-scripts/config.json")
        if latest_config.status_code != 200:
            self.logger.error(f"Something went wrong and launcher cannot get the version")
            return

        data = latest_config.json()
        latest_version = data["Version"]
        local_version = self.config["Version"]
        self.logger.info(f"Installed: {local_version} | Latest: {latest_version}")

        if local_version != latest_version:
            self.logger.info(f"New update: {latest_version}! \nVisit https://github.com/sionit1337/sigma-bot")

        else:
            self.logger.info("No updates found")


    def start_bot(self):
        self.logger.info("Starting bot...")
        os.system(f"python {os.path.abspath("bot/main.py")}")


    def start_launcher(self):
        os.system("cls" if os.name == "nt" else "clear")
        self.logger.info("Launcher has started")
        print("You're using Sigma Bot! Don't forget to star the repository!")

        self.check_updates()
        self.check_config()



if __name__ == "__main__":
    launcher = Launcher()

    try:
        launcher.start_launcher()

    except Exception as e:
        print(f"Something went wrong! \n{e}")