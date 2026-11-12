import json
import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "version_info.json", encoding="utf-8") as file:
    info = json.load(file)

version = info["id"]
client = info["downloads"]["client"]

folder = ROOT / "game_files" / "versions" / version
folder.mkdir(parents=True, exist_ok=True)

target = folder / f"{version}.jar"

print("STAR CLIENT")
print("Downloading Minecraft", version)

request = urllib.request.Request(
    client["url"],
    headers={"User-Agent": "STAR-CLIENT/0.1"}
)

with urllib.request.urlopen(request, timeout=60) as response:
    content = response.read()

if hashlib.sha1(content).hexdigest() != client["sha1"]:
    raise ValueError("SHA1 verification failed!")

target.write_bytes(content)

print("Download complete!")
print("SHA1 verified!")
print("Saved to:", target)
