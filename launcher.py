from json import load
import os
import re
import requests

with open("src/not-scripts/config.json", "r") as file:
    config = load(file)


def check_config():
    print("Checking config for token...")

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
    local_version_minor = int(local_version_splitted[0])

    latest_version_major = int(latest_version_splitted[1])
    latest_version_minor = int(latest_version_splitted[1])

    # TODO make download on every major version
    match (latest_version_major > local_version_major, latest_version_minor > local_version_minor):
        case (False, False):
            print("No updates found!")

        case (False, True):
            print(f"New minor version: {latest_version}! \nVisit https://github.com/sionit1337/sigma-bot")

        case (True, False) | (True, True):
            print(f"New major version: {latest_version}! \nVisit https://github.com/sionit1337/sigma-bot")

        case _:
            print("what")


def start():
    os.system(f"pip install -r {os.abspath("requirements.txt")} -U")
    os.system(f"python {os.abspath("src/main.py")}")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("Hello! You're using Sigma Bot! \nDon't forget to star the repository!")

    check_updates()

    check_config()