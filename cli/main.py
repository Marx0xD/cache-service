import json
import sys

import httpx

from cli.settings import CliSettings


def read_input(settings: CliSettings) -> dict:
    if settings.json_input:
        return json.loads(settings.json_input)
    if settings.input == "-":
        return json.load(sys.stdin)

    if settings.input:
        with open(settings.input, "r") as file:
            return json.load(file)

    raise ValueError("No input provided")


def create_payload(
    client: httpx.Client,
    host: str,
    payload: dict,
) -> int:
    response = client.post(
        f"{host}/payload",
        json=payload,
    )
    response.raise_for_status()

    return response.json()["id"]


def get_payload(
    client: httpx.Client,
    host: str,
    payload_id: int,
) -> dict:
    response = client.get(f"{host}/payload/{payload_id}")
    response.raise_for_status()

    return response.json()


def write_output(settings: CliSettings, result: dict) -> None:
    output = json.dumps(result)

    if settings.output == "-":
        print(output)
        return

    with open(settings.output, "w") as file:
        file.write(output)


def main() -> None:
    settings = CliSettings()
    input_data = read_input(settings=settings)

    with httpx.Client() as client:
        for _ in range(settings.repeat):
            payload_id = create_payload(
                client=client,
                host=settings.host,
                payload=input_data,
            )

            result = get_payload(
                client=client,
                host=settings.host,
                payload_id=payload_id,
            )

    write_output(settings, result)


if __name__ == "__main__":
    main()
