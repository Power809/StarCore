import json

try:
    from .paths import GAME_ROOT
except ImportError:
    from paths import GAME_ROOT

VERSIONS = GAME_ROOT / "versions"


def version_folder(version_id):
    if not version_id or any(
        part in version_id for part in ("/", "\\", "..")
    ):
        raise ValueError("Invalid Minecraft version")

    return VERSIONS / version_id


def save_version_info(version_id, data):
    if data.get("id") != version_id:
        raise ValueError("Version ID mismatch")

    folder = version_folder(version_id)
    folder.mkdir(parents=True, exist_ok=True)

    target = folder / "version.json"
    temporary = target.with_suffix(".json.tmp")

    temporary.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8"
    )

    temporary.replace(target)
    return target


def load_version_info(version_id):
    target = version_folder(version_id) / "version.json"

    if not target.is_file():
        raise FileNotFoundError(target)

    with target.open(encoding="utf-8") as file:
        data = json.load(file)

    if data.get("id") != version_id:
        raise ValueError("Stored version ID mismatch")

    return data
