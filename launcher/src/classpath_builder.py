import json
from pathlib import Path
try:
    from .argument_builder import allowed
except ImportError:
    from argument_builder import allowed

ROOT = Path(__file__).resolve().parents[2]
LIBRARIES = ROOT / "game_files" / "libraries"
VERSION_INFO = ROOT / "version_info.json"


def build_classpath(target="windows", target_arch="x86_64"):
    with VERSION_INFO.open(encoding="utf-8") as f:
        data = json.load(f)

    version = data.get("id", "1.20.1")
    paths = []
    missing = []

    for library in data.get("libraries", []):
        if not allowed(
            library.get("rules"),
            target,
            target_arch
        ):
            continue

        artifact = library.get("downloads", {}).get("artifact")

        if not artifact:
            continue

        relative_path = Path(artifact["path"])
        path = LIBRARIES / relative_path

        if path.is_file():
            paths.append(str(path.resolve()))
        else:
            missing.append(artifact["path"])

    client = ROOT / "game_files" / "versions" / version / f"{version}.jar"

    if client.is_file():
        paths.append(str(client.resolve()))
    else:
        missing.append(str(client))

    return paths, missing


if __name__ == "__main__":
    classpath, missing = build_classpath()

    print("Classpath entries:", len(classpath))
    print("Missing files:", len(missing))

    for item in missing:
        print("MISSING:", item)

    print("Target: Windows x64")
