# Cache Service

Cache Service is a small FastAPI application that transforms paired string
lists to uppercase and stores the generated payload. It includes a command-line
client for submitting payloads and retrieving their output.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- Docker (optional)

## Install

```bash
uv sync
```

## Run the API

```bash
uv run uvicorn backend.src.main:app --host 0.0.0.0 --port 8000
```

## API

- `POST /payload` creates or reuses a payload and returns its ID.
- `GET /payload/{id}` returns the generated output.

Example:

```bash
curl -X POST http://localhost:8000/payload \
  -H 'Content-Type: application/json' \
  -d '{"list_1":["hello"],"list_2":["world"]}'
```

## CLI

Submit inline JSON and print the result:

```bash
uv run cache-cli --json '{"list_1":["hello"],"list_2":["world"]}'
```

Read from a file:

```bash
uv run cache-cli --input payload.json
```

Read from standard input:

```bash
cat payload.json | uv run cache-cli --input -
```

Write to a file (use `--output -` for standard output):

```bash
uv run cache-cli --input payload.json --output result.json
```

Repeat the POST/GET cycle:

```bash
uv run cache-cli --input payload.json --repeat 3
```

## Tests

```bash
uv run pytest
```

## Docker

```bash
docker build -t cache-service .
docker run --rm -p 8000:8000 cache-service
```

## Implementation note

Transformer results are persisted in SQLite, and request hashes allow identical
payload requests to reuse an existing payload ID.
