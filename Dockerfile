FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    git \
    ssh \
    gcc \
    libc-dev \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*



RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
COPY playground /app/playground
COPY pyproject.toml /app/
COPY uv.lock /app/
COPY README.md /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev



ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
ARG PROJECT_NAME
COPY ./infra/${PROJECT_NAME}/start.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN cat /entrypoint.sh

CMD ["/entrypoint.sh"]
