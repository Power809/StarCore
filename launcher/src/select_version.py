import json
from urllib.request import urlopen
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

print("=== STAR CLIENT ===")

try:
    with urlopen(URL, timeout=30) as response:
        manifest = json.load(response)

    version_id = input("Minecraft version: ").strip()

    for old, new in zip("۰۱۲۳۴۵۶۷۸۹", "0123456789"):
        version_id = version_id.replace(old, new)

    for old, new in zip("٠١٢٣٤٥٦٧٨٩", "0123456789"):
        version_id = version_id.replace(old, new)

    selected = next(
        (v for v in manifest["versions"] if v["id"] == version_id),
        None
    )

    if selected:
        with (ROOT / "selected_version.json").open("w") as file:
            json.dump(selected, file, indent=4)

        print("Version selected:", version_id)
        print("Saved successfully!")
    else:
        print("Version not found:", version_id)

except Exception as error:
    print("Error:", error)
