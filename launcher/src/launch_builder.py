import json
from pathlib import Path, PureWindowsPath

try:
    from .argument_builder import read_arguments
    from .classpath_builder import build_classpath
    from .variable_resolver import resolve_arguments
except ImportError:
    from argument_builder import read_arguments
    from classpath_builder import build_classpath
    from variable_resolver import resolve_arguments

ROOT = Path(__file__).resolve().parents[2]
VERSION = "1.20.1"


def windows_path(path, install_root):
    relative = Path(path).resolve().relative_to(ROOT)
    return str(PureWindowsPath(install_root) / PureWindowsPath(*relative.parts))


def build_launch_command(auth, install_root=r"C:\STARCORE"):
    with (ROOT / "version_info.json").open(encoding="utf-8") as f:
        info = json.load(f)

    classpath, missing = build_classpath("windows", "x86_64")

    if missing:
        raise FileNotFoundError(missing)

    version = info.get("id", VERSION)
    native_path = ROOT / "game_files" / "versions" / version / "natives" / "windows_x64"

    dlls = list(native_path.glob("*.dll"))

    if len(dlls) != 7:
        raise FileNotFoundError("Windows x64 native DLL files are incomplete")

    variables = {
        "auth_player_name": auth["username"],
        "version_name": version,
        "game_directory": str(
            PureWindowsPath(install_root) / "game_files" / "instances" / version
        ),
        "assets_root": str(
            PureWindowsPath(install_root) / "game_files" / "assets"
        ),
        "assets_index_name": info["assetIndex"]["id"],
        "auth_uuid": auth["uuid"],
        "auth_access_token": auth["access_token"],
        "user_type": auth["user_type"],
        "version_type": info.get("type", "release"),
        "clientid": auth.get("clientid", ""),
        "auth_xuid": auth.get("xuid", ""),
        "natives_directory": windows_path(native_path, install_root),
        "launcher_name": "STARCORE",
        "launcher_version": "0.1.0",
        "classpath": ";".join(
            windows_path(path, install_root) for path in classpath
        ),
        "resolution_width": "1280",
        "resolution_height": "720",
        "quickPlayPath": "",
        "quickPlaySingleplayer": "",
        "quickPlayMultiplayer": "",
        "quickPlayRealms": ""
    }

    arguments = read_arguments("windows", "x86_64")

    jvm = resolve_arguments(arguments["jvm"], variables)
    game = resolve_arguments(arguments["game"], variables)

    command = ["java", *jvm, info["mainClass"], *game]

    if any("${" in arg for arg in command):
        raise ValueError("Unresolved launch variable")

    return command, variables


if __name__ == "__main__":
    test_auth = {
        "username": "STARCORE_TEST",
        "uuid": "00000000000000000000000000000000",
        "access_token": "TEST_ONLY_INVALID_TOKEN",
        "user_type": "msa",
        "clientid": "TEST_ONLY",
        "xuid": "TEST_ONLY"
    }

    command, variables = build_launch_command(test_auth)

    print("STARCORE Launch Builder")
    print("Target: Windows x64")
    print("Java:", command[0])
    print("Main class:", command[command.index("net.minecraft.client.main.Main")])
    print("Total arguments:", len(command))
    print("Classpath entries:", len(variables["classpath"].split(";")))
    print("Native DLLs: 7")
    print("Unresolved variables:", sum("${" in arg for arg in command))
    print("Build test: SUCCESS")
    print("Execution: DISABLED")
