import json
from pathlib import Path
from urllib.request import urlopen

URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
ROOT = Path(__file__).resolve().parents[2]

def fetch_versions(version_type="release"):
    with urlopen(URL, timeout=20) as response:
        manifest = json.load(response)

    versions = [
        item["id"]
        for item in manifest["versions"]
        if item["type"] == version_type
    ]

    return {
        "latest": manifest["latest"][version_type],
        "versions": versions
    }

def save_version(version_id, root=None):
    with urlopen(URL, timeout=20) as response:
        manifest = json.load(response)

    selected = next(
        (item for item in manifest["versions"] if item["id"] == version_id),
        None
    )

    if selected is None:
        raise ValueError("Minecraft version not found.")

    folder = Path(root) if root else ROOT
    folder.mkdir(parents=True, exist_ok=True)

    with (folder / "selected_version.json").open("w", encoding="utf-8") as file:
        json.dump(selected, file, indent=4)

    return selected
