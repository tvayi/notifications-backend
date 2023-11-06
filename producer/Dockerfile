ARG BASE_CONTAINER=python:3.8

FROM --platform=linux/amd64 $BASE_CONTAINER

USER root
RUN apt-get update && apt-get install -y && apt-get clean

WORKDIR /producer

COPY requirements.txt .
COPY app.py .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./api ./api

CMD ["python", "-m", "api"]
