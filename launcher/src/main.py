import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config.json"

def main():
    with CONFIG.open("r", encoding="utf-8") as file:
        config = json.load(file)

    print("=" * 32)
    print(config["name"])
    print("Version:", config["version"])
    print("Platform:", config["platform"])
    print("Minecraft:", config["minecraft"])
    print("Loaders:", ", ".join(config["loaders"]))
    print("=" * 32)

if __name__ == "__main__":
    main()
