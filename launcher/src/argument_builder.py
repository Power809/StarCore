import json
import platform
import re
from pathlib import Path

try:
    from .version_store import load_version_info
except ImportError:
    from version_store import load_version_info



def os_name(target=None):
    system = (target or platform.system()).lower()

    if system in ("windows", "win32"):
        return "windows"
    if system in ("darwin", "mac", "osx"):
        return "osx"
    return "linux"


def rule_matches(rule, target=None, target_arch="x86_64",
                 features=None, target_os_version=None):
    os_rule = rule.get("os", {})

    if os_rule.get("name") and os_rule["name"] != os_name(target):
        return False

    arch = os_rule.get("arch")
    if arch:
        if not re.search(arch, target_arch, re.IGNORECASE):
            return False

    version = os_rule.get("version")
    if version:
        if target_os_version is None:
            return False
        if not re.search(version, target_os_version):
            return False

    for key, expected in rule.get("features", {}).items():
        if (features or {}).get(key, False) != expected:
            return False

    return True


def allowed(rules, target=None, target_arch="x86_64",
            features=None, target_os_version=None):
    if not rules:
        return True

    result = False

    for rule in rules:
        if rule_matches(
            rule,
            target,
            target_arch,
            features,
            target_os_version
        ):
            result = rule.get("action") == "allow"

    return result


def read_arguments(version_id, target=None, target_arch="x86_64",
                   features=None, target_os_version=None):
    data = load_version_info(version_id)

    result = {"jvm": [], "game": []}

    for section in ("jvm", "game"):
        for item in data.get("arguments", {}).get(section, []):
            if isinstance(item, str):
                result[section].append(item)
                continue

            if allowed(
                item.get("rules"),
                target,
                target_arch,
                features,
                target_os_version
            ):
                value = item.get("value", [])
                result[section].extend(
                    value if isinstance(value, list) else [value]
                )

    return result


if __name__ == "__main__":
    args = read_arguments("1.20.1", "windows", "x86_64")

    print("JVM arguments:", len(args["jvm"]))
    print("Game arguments:", len(args["game"]))
    print("Target platform:", os_name("windows"))
    print("Target architecture: x86_64")
    print("\nJVM:")
    for arg in args["jvm"]:
        print(arg)
    print("\nGame:")
    print(args["game"])
