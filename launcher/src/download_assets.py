import json
import hashlib
import urllib.request
import time
from pathlib import Path
from urllib.error import URLError
from http.client import RemoteDisconnected

try:
    from .version_store import load_version_info
    from .paths import GAME_ROOT
except ImportError:
    from version_store import load_version_info
    from paths import GAME_ROOT

ASSETS = GAME_ROOT / "assets"


def file_sha1(path):
    digest = hashlib.sha1()
    with path.open("rb") as file:
        while True:
            chunk = file.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def download(url, target, expected=None):
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.is_file() and expected:
        if file_sha1(target) == expected:
            return False

    temporary = target.with_suffix(target.suffix + ".part")

    for attempt in range(4):
        try:
            request = urllib.request.Request(
                url,
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
                raise ValueError("SHA1 verification failed")

            temporary.replace(target)
            return True

        except (URLError, RemoteDisconnected, TimeoutError, OSError):
            temporary.unlink(missing_ok=True)
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))

        except Exception:
            temporary.unlink(missing_ok=True)
            raise

    return False


def main(version_id):
    info = load_version_info(version_id)
    index = info["assetIndex"]

    index_path = ASSETS / "indexes" / (index["id"] + ".json")

    download(index["url"], index_path, index.get("sha1"))

    with index_path.open(encoding="utf-8") as file:
        data = json.load(file)

    objects = data["objects"]
    total = len(objects)
    downloaded = 0
    skipped = 0

    print("STARCORE - Downloading assets")
    print("Minecraft:", version_id)
    print("Total assets:", total)

    for name, item in objects.items():
        digest = item["hash"]

        if len(digest) != 40 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("Invalid asset hash: " + name)

        target = ASSETS / "objects" / digest[:2] / digest
        url = "https://resources.download.minecraft.net/" + digest[:2] + "/" + digest

        if download(url, target, digest):
            downloaded += 1
        else:
            skipped += 1

        done = downloaded + skipped
        if done % 100 == 0 or done == total:
            print("Progress:", done, "/", total)

    print("Finished!")
    print("Downloaded:", downloaded)
    print("Already verified:", skipped)


if __name__ == "__main__":
    main("1.20.1")
