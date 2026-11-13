import json
import urllib.request

try:
    from .version_store import save_version_info
    from .paths import DATA_ROOT
except ImportError:
    from version_store import save_version_info
    from paths import DATA_ROOT


def download_version_info(version_id=None):
    selected_path = DATA_ROOT / "selected_version.json"

    with selected_path.open(encoding="utf-8") as file:
        version = json.load(file)

    selected_id = version["id"]

    if version_id and version_id != selected_id:
        raise ValueError("Selected version mismatch")

    request = urllib.request.Request(
        version["url"],
        headers={"User-Agent": "STARCORE/0.1"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)

    path = save_version_info(selected_id, data)

    print("STARCORE")
    print("Version:", selected_id)
    print("Main class:", data["mainClass"])
    print("Libraries:", len(data["libraries"]))
    print("Saved:", path)

    return data


if __name__ == "__main__":
    download_version_info()
