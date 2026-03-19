import yaml
import os

CONFIG_PATH = "plugins.yml"

def main():
    token = os.environ["GH_PAT"]

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    os.makedirs("plugins", exist_ok=True)

    for plugin in config["plugins"]:
        name = plugin["name"]
        repo = plugin["repo"]

        cmd = (
            f'git -c http.extraheader="AUTHORIZATION: bearer {token}" '
            f'clone https://github.com/{repo}.git plugins/{name}'
        )

        print(f"[CLONE] {repo}")
        os.system(cmd)


if __name__ == "__main__":
    main()
