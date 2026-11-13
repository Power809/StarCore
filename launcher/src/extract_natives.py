import shutil
import zipfile
from pathlib import Path, PurePosixPath

try:
    from .version_store import load_version_info
    from .argument_builder import allowed
    from .paths import GAME_ROOT
except ImportError:
    from version_store import load_version_info
    from argument_builder import allowed
    from paths import GAME_ROOT

LIBRARIES = GAME_ROOT / "libraries"


def extract_natives(version_id, target="windows", target_arch="x86_64"):
    info = load_version_info(version_id)

    output = (
        GAME_ROOT / "versions" /
        version_id / "natives" / f"{target}_{target_arch}"
    )

    output.mkdir(parents=True, exist_ok=True)

    jars = []
    extracted = 0

    for library in info.get("libraries", []):
        if not allowed(library.get("rules"), target, target_arch):
            continue

        natives = library.get("natives", {})
        native_key = natives.get(target)

        if not native_key:
            continue

        arch_value = "64" if target_arch == "x86_64" else "32"
        native_key = native_key.replace("${arch}", arch_value)

        classifier = (
            library.get("downloads", {})
            .get("classifiers", {})
            .get(native_key)
        )

        if not classifier:
            continue

        jar = LIBRARIES / classifier["path"]

        if not jar.is_file():
            continue

        jars.append(jar)

        excludes = library.get("extract", {}).get("exclude", [])

        with zipfile.ZipFile(jar) as archive:
            for item in archive.infolist():
                if item.is_dir():
                    continue

                relative = PurePosixPath(item.filename.replace("\\", "/"))

                if relative.is_absolute() or ".." in relative.parts:
                    continue

                if relative.parts and ":" in relative.parts[0]:
                    continue

                if relative.parts and relative.parts[0] == "META-INF":
                    continue

                if any(
                    item.filename.startswith(exclude)
                    for exclude in excludes
                ):
                    continue

                target_file = (output / Path(*relative.parts)).resolve()

                if output.resolve() not in target_file.parents:
                    continue

                target_file.parent.mkdir(parents=True, exist_ok=True)

                with archive.open(item) as source:
                    with target_file.open("wb") as destination:
                        shutil.copyfileobj(source, destination)

                extracted += 1

    print("Minecraft:", version_id)
    print("Native JARs:", len(jars))
    print("Extracted files:", extracted)
    print("Output:", output)

    return output


if __name__ == "__main__":
    extract_natives("1.20.1")
