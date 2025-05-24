FROM python:3.13.3-alpine3.21
LABEL maintainer="raw-marketplace@googlegroups.com"

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    musl-dev \
    gcc \
    python3-dev \
    postgresql-dev \
    curl \
    bash

WORKDIR /backend

COPY django-entrypoint.sh /usr/local/bin/django-entrypoint.sh
RUN chmod +x /usr/local/bin/django-entrypoint.sh

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --no-interaction --no-ansi

COPY . .

RUN mkdir -p /backend/files/media \
    && adduser --disabled-password --no-create-home docker \
    && chown -R docker /backend/files/media \
    && chmod -R 755 /backend/files/media

USER docker
