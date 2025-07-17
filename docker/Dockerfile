# syntax = docker/dockerfile:1
ARG PYTHON_VERSION="3.11"
ARG DEBIAN_VERSION="bullseye"
ARG POETRY_VERSION="1.7.0"

FROM python:${PYTHON_VERSION}-slim-${DEBIAN_VERSION} AS base

ARG APP_UID=1000
ARG APP_GID=1000
ARG PROJECT_PATH="/app"

ARG RUNTIME_DEPS="python3-dev build-essential tzdata curl gosu gettext libpq-dev postgresql-client"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --gid "${APP_GID}" app_group \
  && useradd --system -m -d "${PROJECT_PATH}" -u "${APP_UID}" -g "${APP_GID}" app_user

WORKDIR "${PROJECT_PATH}"

FROM base

RUN apt-get update \
  && apt-get install -y --no-install-recommends ${RUNTIME_DEPS} \
  && rm -rf /usr/share/man \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY --chown=${APP_UID}:${APP_GID} pyproject.toml poetry.lock "${PROJECT_PATH}/"

RUN python -m pip install --no-cache-dir --upgrade pip \
  && python -m pip install --no-cache-dir -U poetry \
  && poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-root \
  && pip uninstall --yes poetry

COPY --chown=${APP_UID}:${APP_GID} . "${PROJECT_PATH}/"

EXPOSE 50051  

USER "${APP_UID}:${APP_GID}"

ENTRYPOINT ["bash", "./docker/start"]

CMD ["start"]
