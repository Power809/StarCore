import platform
import re
import subprocess
from pathlib import Path

try:
    from .classpath_builder import build_classpath
except ImportError:
    from classpath_builder import build_classpath

ROOT = Path(__file__).resolve().parents[2]
VERSION = "1.20.1"


def check_java():
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

        if version < 17:
            return False, f"Java {version} is too old"

        return True, f"Java {version}"

    except Exception as error:
        return False, str(error)


def run_checks():
    checks = []

    checks.append((
        "Windows platform",
        platform.system() == "Windows",
        platform.system()
    ))

    java_ok, java_info = check_java()
    checks.append(("Java 17+", java_ok, java_info))

    client = ROOT / "game_files" / "versions" / VERSION / f"{VERSION}.jar"
    checks.append(("Minecraft client", client.is_file(), str(client)))

    classpath, missing = build_classpath("windows", "x86_64")
    checks.append((
        "Libraries",
        len(classpath) == 65 and not missing,
        f"{len(classpath)} found, {len(missing)} missing"
    ))

    natives = ROOT / "game_files" / "versions" / VERSION / "natives" / "windows_x64"
    dlls = list(natives.glob("*.dll")) if natives.is_dir() else []

    checks.append((
        "Native DLL files",
        len(dlls) == 7,
        f"{len(dlls)} found"
    ))

    assets_index = ROOT / "game_files" / "assets" / "indexes" / "5.json"
    checks.append((
        "Assets index",
        assets_index.is_file(),
        str(assets_index)
    ))

    for name, passed, detail in checks:
        print(("PASS" if passed else "FAIL"), name, "-", detail)

    print()
    print("Result:", "READY" if all(item[1] for item in checks) else "NOT READY")


if __name__ == "__main__":
    run_checks()
