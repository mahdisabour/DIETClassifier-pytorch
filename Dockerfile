FROM python:3.10.12

ARG GITHUB_TOKEN
WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://${GITHUB_TOKEN}@github.com/AdanAITeam/monitoring-client.git@main

COPY ./src/ ./src/
COPY ./demo/ ./demo/

