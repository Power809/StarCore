import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIBRARIES = ROOT / "game_files" / "libraries"
OUTPUT = ROOT / "game_files" / "versions" / "1.20.1" / "natives"

OUTPUT.mkdir(parents=True, exist_ok=True)

jars = list(LIBRARIES.rglob("*-natives-windows.jar"))
extracted = 0

for jar in jars:
    with zipfile.ZipFile(jar) as archive:
        for item in archive.infolist():
            if item.is_dir() or item.filename.startswith("META-INF/"):
                continue

            target = (OUTPUT / item.filename).resolve()

            if OUTPUT.resolve() not in target.parents:
                continue

            target.parent.mkdir(parents=True, exist_ok=True)

            with archive.open(item) as source, target.open("wb") as dest:
                dest.write(source.read())

            extracted += 1

print("Native JARs:", len(jars))
print("Extracted files:", extracted)
print("Output:", OUTPUT)
