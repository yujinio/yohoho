# --- Builder stage ---
FROM python:3.11.4 as builder

RUN pip install --no-cache poetry && apt-get update && apt-get install -y --no-install-recommends cmake && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./
COPY ./yohoho ./yohoho

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --only main --no-root

# --- Runtime stage ---
FROM python:3.11.4-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PROJECT_PATH=/app

RUN useradd -u 1000 /app

COPY --chown=1000 --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --chown=1000 ./yohoho ${PROJECT_PATH}/yohoho

USER 1000
EXPOSE 5000

WORKDIR ${PROJECT_PATH}

CMD [ "python", "-m", "gunicorn", "-c", "yohoho/gunicorn.conf.py", "yohoho.app:create_app()" ]
