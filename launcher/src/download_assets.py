import json
import hashlib
import urllib.request
import time
from pathlib import Path
from urllib.error import URLError
from http.client import RemoteDisconnected

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "game_files" / "assets"

def download(url, target, expected=None):
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and expected:
        if hashlib.sha1(target.read_bytes()).hexdigest() == expected:
            return False

    temporary = target.with_suffix(target.suffix + ".part")

    for attempt in range(4):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "STAR-CLIENT/0.1"}
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
                temporary.unlink(missing_ok=True)
                raise ValueError("SHA1 verification failed")

            temporary.replace(target)
            return True

        except (URLError, RemoteDisconnected, TimeoutError, OSError):
            temporary.unlink(missing_ok=True)
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))

    return False

def main():
    with (ROOT / "version_info.json").open(encoding="utf-8") as file:
        info = json.load(file)

    index = info["assetIndex"]
    index_path = ASSETS / "indexes" / (index["id"] + ".json")

    download(index["url"], index_path, index.get("sha1"))

    with index_path.open(encoding="utf-8") as file:
        data = json.load(file)

    objects = data["objects"]
    total = len(objects)
    downloaded = 0
    skipped = 0

    print("STAR CLIENT - Downloading assets")
    print("Total assets:", total)

    for name, item in objects.items():
        digest = item["hash"]
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
    main()
