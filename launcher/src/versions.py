import json
from urllib.request import urlopen

URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

def main():
    print("STAR CLIENT - Minecraft Version Manager")
    print("-" * 40)

    try:
        with urlopen(URL, timeout=20) as response:
            data = json.load(response)

        print("Latest Release:", data["latest"]["release"])
        print("Latest Snapshot:", data["latest"]["snapshot"])
        print("\nRecent Minecraft Releases:\n")

        releases = [
            version["id"]
            for version in data["versions"]
            if version["type"] == "release"
        ]

        for version in releases[:20]:
            print("-", version)

    except Exception as error:
        print("Could not connect:", error)

if __name__ == "__main__":
    main()
