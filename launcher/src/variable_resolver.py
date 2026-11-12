import re

PATTERN = re.compile(r"\$\{([^}]+)\}")


def resolve_value(value, variables):
    def replace(match):
        name = match.group(1)

        if name not in variables:
            raise ValueError(f"Missing variable: {name}")

        result = variables[name]

        if result is None:
            raise ValueError(f"Empty variable: {name}")

        return str(result)

    return PATTERN.sub(replace, value)


def resolve_arguments(arguments, variables):
    return [
        resolve_value(arg, variables)
        for arg in arguments
    ]


if __name__ == "__main__":
    test_variables = {
        "auth_player_name": "STARCORE_Player",
        "version_name": "1.20.1",
        "natives_directory": "/test/natives",
        "classpath": "/test/client.jar"
    }

    test_arguments = [
        "${auth_player_name}",
        "${version_name}",
        "-Djava.library.path=${natives_directory}",
        "${classpath}"
    ]

    result = resolve_arguments(test_arguments, test_variables)

    print("Variable Resolver: OK")
    for item in result:
        print(item)
