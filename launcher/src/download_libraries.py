import json
import hashlib
import urllib.request
import time
from pathlib import Path
from urllib.error import URLError
from http.client import RemoteDisconnected

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "game_files" / "libraries"
OS_NAME = "windows"
ARCH = "64"

def allowed(library):
    rules = library.get("rules")
    if not rules:
        return True

    result = False

    for rule in rules:
        os_rule = rule.get("os", {})
        matches = not os_rule.get("name") or os_rule["name"] == OS_NAME

        if os_rule.get("arch"):
            matches = matches and os_rule["arch"] in ("x86", "x86_64")

        if matches:
            result = rule["action"] == "allow"

    return result

def download(item):
    relative = item["path"]
    target = BASE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    expected = item.get("sha1")

    if target.exists() and expected:
        digest = hashlib.sha1(target.read_bytes()).hexdigest()
        if digest == expected:
            return False

    temporary = target.with_suffix(target.suffix + ".part")

    for attempt in range(4):
        try:
            request = urllib.request.Request(
                item["url"],
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
                raise ValueError("SHA1 verification failed: " + relative)

            temporary.replace(target)
            return True

        except (URLError, RemoteDisconnected, TimeoutError, OSError) as error:
            temporary.unlink(missing_ok=True)
            if attempt == 3:
                raise RuntimeError("Download failed: " + relative) from error
            print("Connection interrupted. Retrying:", attempt + 1)
            time.sleep(3 * (attempt + 1))

    return False

def main():
    with (ROOT / "version_info.json").open(encoding="utf-8") as file:
        info = json.load(file)

    downloaded = 0
    skipped = 0

    print("STAR CLIENT - Windows 64-bit")
    print("Downloading libraries...")

    for library in info["libraries"]:
        if not allowed(library):
            continue

        downloads = library.get("downloads", {})
        items = []

        artifact = downloads.get("artifact")
        if artifact:
            items.append(artifact)

        natives = library.get("natives", {})
        native_key = natives.get(OS_NAME, "").replace("${arch}", ARCH)
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
    main()
