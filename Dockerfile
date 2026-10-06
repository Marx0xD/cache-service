FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md ./
COPY backend ./backend
COPY cli ./cli

RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
