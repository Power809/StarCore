from pathlib import Path

try:
    from .version_store import load_version_info
    from .argument_builder import allowed
    from .paths import GAME_ROOT
except ImportError:
    from version_store import load_version_info
    from argument_builder import allowed
    from paths import GAME_ROOT

LIBRARIES = GAME_ROOT / "libraries"


def build_classpath(version_id, target="windows", target_arch="x86_64"):
    data = load_version_info(version_id)

    paths = []
    missing = []

    for library in data.get("libraries", []):
        if not allowed(library.get("rules"), target, target_arch):
            continue

        artifact = library.get("downloads", {}).get("artifact")

        if not artifact:
            continue

        relative_path = Path(artifact["path"])

        if relative_path.is_absolute() or ".." in relative_path.parts:
            missing.append(artifact["path"])
            continue

        path = LIBRARIES / relative_path

        if path.is_file():
            paths.append(str(path.resolve()))
        else:
            missing.append(artifact["path"])

    client = GAME_ROOT / "versions" / version_id / f"{version_id}.jar"

    if client.is_file():
        paths.append(str(client.resolve()))
    else:
        missing.append(str(client))

    return paths, missing
