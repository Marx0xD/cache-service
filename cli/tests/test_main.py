import io
import json
import sys
from unittest.mock import Mock

import httpx

from cli import main as cli_main
from cli.settings import CliSettings


PAYLOAD = {"list_1": ["hello"], "list_2": ["world"]}


def test_reads_inline_json():
    settings = CliSettings(
        _cli_parse_args=["--json", json.dumps(PAYLOAD)]
    )

    assert cli_main.read_input(settings) == PAYLOAD


def test_reads_input_file(tmp_path):
    input_path = tmp_path / "payload.json"
    input_path.write_text(json.dumps(PAYLOAD))
    settings = CliSettings(
        _cli_parse_args=["--input", str(input_path)]
    )

    assert cli_main.read_input(settings) == PAYLOAD


def test_reads_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(PAYLOAD)))
    settings = CliSettings(_cli_parse_args=["--input", "-"])

    assert cli_main.read_input(settings) == PAYLOAD


def test_writes_output_file(tmp_path):
    output_path = tmp_path / "result.json"
    settings = CliSettings(
        _cli_parse_args=[
            "--json",
            json.dumps(PAYLOAD),
            "--output",
            str(output_path),
        ]
    )

    cli_main.write_output(settings, {"output": "HELLO, WORLD"})

    assert json.loads(output_path.read_text()) == {
        "output": "HELLO, WORLD"
    }


def test_writes_output_to_stdout(capsys):
    settings = CliSettings(
        _cli_parse_args=["--json", json.dumps(PAYLOAD), "--output", "-"]
    )

    cli_main.write_output(settings, {"output": "HELLO, WORLD"})

    assert json.loads(capsys.readouterr().out) == {
        "output": "HELLO, WORLD"
    }


def test_repeat_runs_post_and_get_for_each_iteration(monkeypatch):
    client = object()
    client_context = Mock()
    client_context.__enter__ = Mock(return_value=client)
    client_context.__exit__ = Mock(return_value=None)
    create_payload = Mock(return_value=7)
    get_payload = Mock(return_value={"output": "HELLO, WORLD"})
    write_output = Mock()

    monkeypatch.setattr(
        sys,
        "argv",
        ["cache-cli", "--json", json.dumps(PAYLOAD), "--repeat", "3"],
    )
    monkeypatch.setattr(cli_main.httpx, "Client", lambda: client_context)
    monkeypatch.setattr(cli_main, "create_payload", create_payload)
    monkeypatch.setattr(cli_main, "get_payload", get_payload)
    monkeypatch.setattr(cli_main, "write_output", write_output)

    cli_main.main()

    assert create_payload.call_count == 3
    assert get_payload.call_count == 3
    write_output.assert_called_once()


def test_posts_payload_and_gets_result_over_http():
    requests = []

    def handle_request(request):
        requests.append(request)
        if request.method == "POST":
            return httpx.Response(200, json={"id": 7})
        return httpx.Response(200, json={"output": "HELLO, WORLD"})

    transport = httpx.MockTransport(handle_request)

    with httpx.Client(transport=transport) as client:
        payload_id = cli_main.create_payload(client, "http://test", PAYLOAD)
        result = cli_main.get_payload(client, "http://test", payload_id)

    assert payload_id == 7
    assert result == {"output": "HELLO, WORLD"}
    assert [request.method for request in requests] == ["POST", "GET"]
    assert requests[0].url == httpx.URL("http://test/payload")
    assert json.loads(requests[0].content) == PAYLOAD
    assert requests[1].url == httpx.URL("http://test/payload/7")
