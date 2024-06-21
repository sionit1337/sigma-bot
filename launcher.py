from json import load
import os
import re
import requests


cfg_path = "./bot/not-scripts/config.json"

with open(cfg_path, "r") as file:
    config = load(file)


class Launcher:
    def __init__(self):
        pass


    def check_config(self):
        print("Checking config for token...")

        pattern = re.compile("[-a-zA-Z0-9_].[-a-zA-Z0-9_].[-a-zA-Z0-9_]")
        match = re.search(pattern, config["Token"])
        if not match:
            print("You didn't inserted bot token")

            config["Token"] = input("Insert here: ")
        
            with open(cfg_path, "w") as file:
                file.write(f"{config}".replace("'", "\""))

            self.download_python_libs()
            
            print("Now restart the launcher")

        else:
            print("All right")
            self.start_bot()


    def check_updates(self):
        print("Checking for updates...")

        latest_config = requests.get("https://raw.githubusercontent.com/sionit1337/sigma-bot/main/src/not-scripts/config.json")
        if latest_config.status_code != 200:
            print(f"Something went wrong and launcher cannot get the version \nStatus code: {latest_config.status_code}")

        data = latest_config.json()
        latest_version = data["Version"]
        local_version = config["Version"]
        print(f"Installed: {local_version} | Latest: {latest_version}")

        if local_version != latest_version:
            print(f"New update: {latest_version}! \nVisit https://github.com/sionit1337/sigma-bot")

        else:
            print("No updates found")


    def download_python_libs(self):
        print("Would you like for launcher to install necessary Python libraries?")
        with open("requirements.txt", "r") as file:
            print(file.read())

        choice = input("[Y]es, [N]o: ")

        match choice.lower():
            case "y":
                print("Trying to download...")
                os.system(f"pip install -r {os.path.abspath("requirements.txt")} -U")

            case "n":
                print("Skipping...")


    def start_bot(self):
        print("Starting now...")

        os.system(f"python {os.path.abspath("bot/main.py")}")


    def start_launcher(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("Hello! You're using Sigma Bot! \nDon't forget to star the repository!")

        self.check_updates()
        self.check_config()



if __name__ == "__main__":
    launcher = Launcher()

    try:
        launcher.start_launcher()

    except Exception as e:
        print(f"Something went wrong! \n{e}")