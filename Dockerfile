FROM python:3.13.3-alpine3.21
LABEL maintainer="raw-marketplace@googlegroups.com"

ENV PYTHONUNBUFFERED 1

# Install dependencies for building Python packages
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

# Set working directory
WORKDIR /backend

# Install Poetry and project dependencies
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project files
COPY . .

# Create and configure media directory
RUN mkdir -p /backend/files/media \
    && adduser --disabled-password --no-create-home docker \
    && chown -R docker /backend/files/media \
    && chmod -R 755 /backend/files/media

USER docker
