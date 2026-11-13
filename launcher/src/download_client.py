import hashlib
import urllib.request

try:
    from .version_store import load_version_info
    from .paths import GAME_ROOT
except ImportError:
    from version_store import load_version_info
    from paths import GAME_ROOT


def download_client(version_id):
    info = load_version_info(version_id)
    client = info["downloads"]["client"]

    folder = GAME_ROOT / "versions" / version_id
    folder.mkdir(parents=True, exist_ok=True)

    target = folder / f"{version_id}.jar"
    temporary = target.with_suffix(".jar.part")

    request = urllib.request.Request(
        client["url"],
        headers={"User-Agent": "STARCORE/0.1"}
    )

    digest = hashlib.sha1()

    print("STARCORE")
    print("Downloading Minecraft", version_id)

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            with temporary.open("wb") as file:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    file.write(chunk)

        if digest.hexdigest() != client["sha1"]:
            raise ValueError("SHA1 verification failed!")

        temporary.replace(target)

    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    print("Download complete!")
    print("SHA1 verified!")
    print("Saved to:", target)

    return target


if __name__ == "__main__":
    download_client("1.20.1")
