from json import load
import os
import re
import requests

with open("src/not-scripts/config.json", "r") as file:
    config = load(file)


class Launcher:
    def __init__(self):
        pass


    def check_config(self):
        print("Checking config for token...")

        pattern = re.compile("([-a-zA-Z0-9_].[-a-zA-Z0-9_].[-a-zA-Z0-9_])")
        match = re.search(pattern, config["Token"])
        if not match:
            print("You didn't inserted bot token")

            config["Token"] = input("Insert here: ")
        
            with open("src/not-scripts/config.json", "w") as file:
                file.write(f"{config}".replace("'", "\""))

            print("Now restart the launcher")

        else:
            print("Starting now...")
            self.start_bot()


    def check_updates(self):
        print("Checking for updates...")

        with open("current-version", "r") as file:
            local_version = file.read()

        repo_version = requests.get("https://raw.githubusercontent.com/sionit1337/sigma-bot/main/current-version")
        if repo_version.status_code != 200:
            print(f"Something went wrong and launcher cannot get the version \nStatus code: {repo_version.status_code}")

        latest_version = repo_version.content.decode("utf-8")
        print(f"Installed: {local_version} | Latest: {latest_version}")

        local_version_splitted = local_version.split(".")
        latest_version_splitted = latest_version.split(".")

        local_version_major = int(local_version_splitted[0])
        local_version_minor = int(local_version_splitted[1])

        latest_version_major = int(latest_version_splitted[0])
        latest_version_minor = int(latest_version_splitted[1])

        match (latest_version_major > local_version_major, latest_version_minor > local_version_minor):
            case (False, False):
                print("No updates found!")

            case (False, True):
                print(f"New minor version: {latest_version}! \nVisit https://github.com/sionit1337/sigma-bot")

            case (True, False) | (True, True):
                print(f"New major version: {latest_version}! \nVisit https://github.com/sionit1337/sigma-bot")

            case _:
                print("what")


    def download_update(self):
        pass # TODO


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
        os.system(f"python {os.path.abspath("src/main.py")}")


    def start_launcher(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("Hello! You're using Sigma Bot! \nDon't forget to star the repository!")

        self.check_updates()
        self.download_python_libs()
        self.check_config()



if __name__ == "__main__":
    launcher = Launcher()

    try:
        launcher.start_launcher()

    except Exception as e:
        print(f"Something went wrong! \n{e}")