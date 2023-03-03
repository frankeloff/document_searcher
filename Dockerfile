FROM python:3.10-slim

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./migrations ./migrations
COPY alembic.ini .