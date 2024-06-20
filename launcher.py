from json import load
import os
import re
import requests

with open("src/not-scripts/config.json", "r") as file:
    config = load(file)


def check_config():
    pattern = re.compile("([-a-zA-Z0-9_]{24}.[-a-zA-Z0-9_]{6}.[-a-zA-Z0-9_]{27})")
    match = re.search(pattern, config["Token"])
    if not match:
        print("You didn't inserted bot token")

        config["Token"] = input("Insert here: ")
    
        with open("src/not-scripts/config.json", "w") as file:
            file.write(f"{config}".replace("'", "\""))

        print("Now restart the launcher")

    else:
        print("Starting now...")
        start()


def check_updates():
    with open("current-version", "r") as file:
        local_version = file.read()

    latest_version = requests.get("https://raw.githubusercontent.com/sionit1337/sigma-bot/main/current_version")
    print(f"{latest_version} | {local_version}")


def start():
    os.system(f"pip install -r {os.abspath("requirements.txt")} -U")
    os.system(f"python {os.abspath("src/main.py")}")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("Hello! You're using Sigma Bot! \nDon't forget to star the repository!")

    print("Checking for updates...")
    check_updates()

    check_config()