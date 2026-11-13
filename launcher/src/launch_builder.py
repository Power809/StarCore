from pathlib import Path

try:
    from .argument_builder import read_arguments
    from .classpath_builder import build_classpath
    from .variable_resolver import resolve_arguments
    from .version_store import load_version_info
    from .paths import GAME_ROOT, DATA_ROOT
except ImportError:
    from argument_builder import read_arguments
    from classpath_builder import build_classpath
    from variable_resolver import resolve_arguments
    from version_store import load_version_info
    from paths import GAME_ROOT, DATA_ROOT


def build_launch_command(auth, version_id):
    info = load_version_info(version_id)

    classpath, missing = build_classpath(
        version_id, "windows", "x86_64"
    )

    if missing:
        raise FileNotFoundError(missing)

    native_path = (
        GAME_ROOT / "versions" / version_id /
        "natives" / "windows_x86_64"
    )

    dlls = list(native_path.glob("*.dll"))

    if len(dlls) != 7:
        raise FileNotFoundError(
            "Windows x64 native DLL files are incomplete"
        )

    instance_path = DATA_ROOT / "instances" / version_id

    variables = {
        "auth_player_name": auth["username"],
        "version_name": version_id,
        "game_directory": str(instance_path),
        "assets_root": str(GAME_ROOT / "assets"),
        "assets_index_name": info["assetIndex"]["id"],
        "auth_uuid": auth["uuid"],
        "auth_access_token": auth["access_token"],
        "user_type": auth["user_type"],
        "version_type": info.get("type", "release"),
        "clientid": auth.get("clientid", ""),
        "auth_xuid": auth.get("xuid", ""),
        "natives_directory": str(native_path.resolve()),
        "launcher_name": "STARCORE",
        "launcher_version": "0.1.0",
        "classpath": ";".join(
            str(Path(path).resolve()) for path in classpath
        ),
        "resolution_width": "1280",
        "resolution_height": "720",
        "quickPlayPath": "",
        "quickPlaySingleplayer": "",
        "quickPlayMultiplayer": "",
        "quickPlayRealms": ""
    }

    arguments = read_arguments(
        version_id, "windows", "x86_64"
    )

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

    command, variables = build_launch_command(
        test_auth, "1.20.1"
    )

    print("STARCORE Launch Builder")
    print("Target: Windows x64")
    print("Java:", command[0])
    print("Main class:", command[command.index(
        "net.minecraft.client.main.Main"
    )])
    print("Total arguments:", len(command))
    print("Classpath entries:", len(
        variables["classpath"].split(";")
    ))
    print("Native DLLs: 7")
    print("Unresolved variables:", sum(
        "${" in arg for arg in command
    ))
    print("Build test: SUCCESS")
    print("Execution: DISABLED")
