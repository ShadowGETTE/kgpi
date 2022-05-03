FROM python:3.7.13-slim-bullseye AS development-build

ARG DJANGO_ENV

ENV DJANGO_ENV=&{DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.0.5 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION" && poetry --version

RUN apt-get update \
  && apt-get install -y \
    libgl1-mesa-glx
RUN apt-get update \
  && apt-get install -y \
    'ffmpeg' \
    'libsm6' \
    'libxext6'

# set work directory
WORKDIR /code
COPY pyproject.toml poetry.lock /code/

RUN pip3 install gunicorn psycopg2

# Install dependencies:
RUN poetry install
# copy project
COPY . .