import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESOURCE_ROOT = Path(
    getattr(sys, "_MEIPASS", PROJECT_ROOT)
)


def get_data_root():
    if os.name == "nt":
        base = Path(
            os.environ.get(
                "APPDATA",
                Path.home() / "AppData" / "Roaming"
            )
        )
        folder = base / "STARCORE"
    else:
        folder = PROJECT_ROOT

    folder.mkdir(parents=True, exist_ok=True)
    return folder


DATA_ROOT = get_data_root()
GAME_ROOT = DATA_ROOT / "game_files"
CONFIG_PATH = RESOURCE_ROOT / "config.json"
