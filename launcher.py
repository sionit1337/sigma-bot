from json import load
import re
import requests

import os
import platform
from importlib.util import find_spec

import subprocess

from bot.logger import Logger
import logging


here = os.path.realpath(os.path.dirname(__file__))

if not os.path.exists(f"{here}/bot/cogs/temp"):
    os.mkdir(f"{here}/bot/cogs/temp")
    
if not os.path.exists(f"{here}/bot/logs"):
    os.mkdir(f"{here}/bot/logs")

logger = Logger(f"{here}/bot/logs", "launcher")
logger.init_logger()

cfg_path = f"{here}/bot/not-scripts/config.json"

with open(cfg_path, "r") as file:
    config = load(file)


class Launcher:
    def __init__(self):
        self.__config = config
        self.logger = logger


    def get_versions(self):
        latest_config = requests.get("https://raw.githubusercontent.com/sionit1337/sigma-bot/main/bot/not-scripts/config.json")

        if latest_config.status_code != 200:
            self.logger.log(f"Something went wrong and launcher cannot get the latest version (HTTP {latest_config.status_code})", logging.ERROR)
            return

        data = latest_config.json()

        latest_version = data["Version"]
        local_version = self.get_config["Version"]

        versions = {
            "Local": local_version,
            "Latest": latest_version
            }

        return versions


    @property
    def get_config(self):
        return self.__config


    def check_config(self):
        self.logger.log("Checking config for token... (with regex)", logging.INFO)

        pattern = re.compile("[a-zA-Z0-9-]+.[a-zA-Z0-9-]+.[a-zA-Z0-9-]+")
        match = re.search(pattern, self.get_config["Token"])

        if not match:
            self.logger.log("Token wasn't found", logging.ERROR)
            return

        self.start_bot()


    def check_updates(self):
        self.logger.log("Checking for updates...", logging.INFO)

        versions = self.get_versions()

        if versions["Local"] != versions["Latest"]:
            self.logger.log(f"Version in repository has been changed: {versions["Latest"]} (maybe an update)", logging.WARN)
            
        else:
            self.logger.log("Latest version is installed", logging.INFO)


    def start_bot(self):
        self.logger.log("Starting bot...", logging.INFO)
        subprocess.run(["python", f"{os.path.abspath("bot/main.py")}"])

    
    def check_modules(self):
        with open("requirements.txt", "r") as file:
            reqs = file.read()
        
        reqs = reqs.split("\n")
        if "" in reqs:
            reqs.remove("")

        reqs_not_installed = []

        for req in reqs:
            if find_spec(req):
                continue
            
            reqs_not_installed.append(req)

        if not reqs_not_installed:
            self.logger.log("All modules installed", logging.INFO)
            return
            
        self.logger.log(f"You haven't installed some requirements: {', '.join(reqs_not_installed)}", logging.WARN)
        self.logger.log("Installing...", logging.INFO)
            
        for req in reqs_not_installed:
            os.system(f"pip install -U {req}")


    def log_info(self):
        self.logger.log(f"OS: {platform.platform()}", logging.INFO)
        self.logger.log(f"Architecture: {platform.architecture()[0]}", logging.INFO)

        self.logger.log(f"Python version: {platform.python_version()}", logging.INFO)

        from disnake import __version__ as disnake_version
        self.logger.log(f"Disnake version: {disnake_version}", logging.INFO)

        versions = self.get_versions()

        self.logger.log(f"Bot version (currently installed): {versions["Local"]}", logging.INFO)
        self.logger.log(f"Bot version (latest found on repo): {versions["Latest"]}", logging.INFO)


    def start_launcher(self):
        os.system("cls" if os.name == "nt" else "clear")
        self.logger.log("Launcher has been started", logging.INFO)

        self.check_modules()
        self.check_updates()
        self.log_info()
        self.check_config()


if __name__ == "__main__":
    launcher = Launcher()

    try:
        launcher.start_launcher()

    except Exception as e:
        launcher.logger.log(f"Something went wrong! \n{e}", logging.ERROR)