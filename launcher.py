from json import load
import os
import re

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


def start():
    os.system(f"pip install -r {os.abspath("requirements.txt")} -U")
    os.system(f"python {os.abspath("src/main.py")}")


if __name__ == "__main__":
    os.system("clear" if os.path.exists("/usr/bin/clear") else "cls")
    print("Hello! You're using Sigma Bot! \nDon't forget to star the repository!")
    check_config()