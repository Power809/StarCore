try:
    from .version_manager import save_version
    from .download_info import download_version_info
    from .download_client import download_client
    from .download_libraries import main as download_libraries
    from .download_assets import main as download_assets
    from .extract_natives import extract_natives
except ImportError:
    from version_manager import save_version
    from download_info import download_version_info
    from download_client import download_client
    from download_libraries import main as download_libraries
    from download_assets import main as download_assets
    from extract_natives import extract_natives


def install_version(version_id):
    print("=" * 40)
    print("STARCORE INSTALLER")
    print("Minecraft:", version_id)
    print("=" * 40)

    print("[1/6] Fetching version information...")
    save_version(version_id)

    print("[2/6] Downloading version metadata...")
    download_version_info(version_id)

    print("[3/6] Downloading Minecraft client...")
    download_client(version_id)

    print("[4/6] Downloading libraries...")
    download_libraries(version_id)

    print("[5/6] Downloading assets...")
    download_assets(version_id)

    print("[6/6] Extracting natives...")
    extract_natives(version_id)

    print("=" * 40)
    print("INSTALLATION COMPLETED")
    print("Version:", version_id)
    print("=" * 40)


if __name__ == "__main__":
    install_version("1.20.1")
