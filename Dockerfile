FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

COPY pyproject.toml uv.lock .


ENV UV_NO_DEV=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN uv sync --locked

COPY src ./src

CMD ["uv", "run", "uvicorn", "src:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

