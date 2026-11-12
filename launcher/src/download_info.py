import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "selected_version.json", encoding="utf-8") as file:
    version = json.load(file)

print("STAR CLIENT")
print("Loading:", version["id"])

request = urllib.request.Request(
    version["url"],
    headers={"User-Agent": "STAR-CLIENT/0.1"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    data = json.load(response)

output = ROOT / "version_info.json"

with open(output, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("Main class:", data["mainClass"])
print("Libraries:", len(data["libraries"]))
print("Version information saved!")
