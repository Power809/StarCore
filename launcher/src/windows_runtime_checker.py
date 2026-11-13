import platform
import re
import subprocess
from pathlib import Path

try:
    from .classpath_builder import build_classpath
    from .version_store import load_version_info
    from .paths import GAME_ROOT
except ImportError:
    from classpath_builder import build_classpath
    from version_store import load_version_info
    from paths import GAME_ROOT



def check_java(required_version):
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stderr + result.stdout
        match = re.search(r'version "(\d+)', output)

        if not match:
            return False, "Java version not detected"

        version = int(match.group(1))

        if version < required_version:
            return False, f"Java {version}, required {required_version}+"

        return True, f"Java {version}"

    except Exception as error:
        return False, str(error)


def run_checks(version_id):
    info = load_version_info(version_id)
    checks = []

    checks.append((
        "Windows platform",
        platform.system() == "Windows",
        platform.system()
    ))

    required_java = info.get("javaVersion", {}).get("majorVersion", 17)
    java_ok, java_info = check_java(required_java)

    checks.append((
        f"Java {required_java}+",
        java_ok,
        java_info
    ))

    client = (
        GAME_ROOT / "versions" /
        version_id / f"{version_id}.jar"
    )

    checks.append((
        "Minecraft client",
        client.is_file(),
        str(client)
    ))

    classpath, missing = build_classpath(
        version_id,
        "windows",
        "x86_64"
    )

    checks.append((
        "Libraries",
        len(classpath) > 0 and not missing,
        f"{len(classpath)} found, {len(missing)} missing"
    ))

    natives = (
        GAME_ROOT / "versions" /
        version_id / "natives" / "windows_x86_64"
    )

    dlls = list(natives.glob("*.dll")) if natives.is_dir() else []

    checks.append((
        "Native DLL files",
        len(dlls) > 0,
        f"{len(dlls)} found"
    ))

    asset_index = info.get("assetIndex", {}).get("id", "")
    assets_index = GAME_ROOT / "assets" / "indexes" / f"{asset_index}.json"

    checks.append((
        "Assets index",
        bool(asset_index) and assets_index.is_file(),
        str(assets_index)
    ))

    for name, passed, detail in checks:
        print(("PASS" if passed else "FAIL"), name, "-", detail)

    print()
    print("Result:", "READY" if all(item[1] for item in checks) else "NOT READY")


if __name__ == "__main__":
    run_checks("1.20.1")
