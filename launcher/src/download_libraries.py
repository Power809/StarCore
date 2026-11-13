import hashlib
import time
import urllib.request
from pathlib import Path
from urllib.error import URLError
from http.client import RemoteDisconnected

try:
    from .version_store import load_version_info
    from .argument_builder import allowed
    from .paths import GAME_ROOT
except ImportError:
    from version_store import load_version_info
    from argument_builder import allowed
    from paths import GAME_ROOT

BASE = GAME_ROOT / "libraries"


def file_sha1(path):
    digest = hashlib.sha1()
    with path.open("rb") as file:
        while True:
            chunk = file.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def download(item):
    relative = Path(item["path"])

    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Invalid library path: " + str(relative))

    target = BASE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    expected = item.get("sha1")

    if target.is_file() and expected:
        if file_sha1(target) == expected:
            return False

    temporary = target.with_suffix(target.suffix + ".part")

    for attempt in range(4):
        try:
            request = urllib.request.Request(
                item["url"],
                headers={"User-Agent": "STARCORE/0.1"}
            )

            digest = hashlib.sha1()

            with urllib.request.urlopen(request, timeout=90) as response:
                with temporary.open("wb") as file:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        file.write(chunk)
                        digest.update(chunk)

            if expected and digest.hexdigest() != expected:
                raise ValueError("SHA1 verification failed: " + str(relative))

            temporary.replace(target)
            return True

        except (URLError, RemoteDisconnected, TimeoutError, OSError) as error:
            temporary.unlink(missing_ok=True)
            if attempt == 3:
                raise RuntimeError("Download failed: " + str(relative)) from error
            print("Connection interrupted. Retrying:", attempt + 1)
            time.sleep(3 * (attempt + 1))

        except Exception:
            temporary.unlink(missing_ok=True)
            raise

    return False


def main(version_id):
    info = load_version_info(version_id)
    downloaded = 0
    skipped = 0

    print("STARCORE - Windows 64-bit")
    print("Minecraft:", version_id)
    print("Downloading libraries...")

    for library in info.get("libraries", []):
        if not allowed(library.get("rules"), "windows", "x86_64"):
            continue

        downloads = library.get("downloads", {})
        items = []

        artifact = downloads.get("artifact")
        if artifact:
            items.append(artifact)

        natives = library.get("natives", {})
        native_key = natives.get("windows", "").replace("${arch}", "64")
        classifier = downloads.get("classifiers", {}).get(native_key)

        if classifier:
            items.append(classifier)

        for item in items:
            if download(item):
                downloaded += 1
                print("Downloaded:", item["path"])
            else:
                skipped += 1

    print("Finished!")
    print("Downloaded:", downloaded)
    print("Already verified:", skipped)


if __name__ == "__main__":
    main("1.20.1")
