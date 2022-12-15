FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y python3
RUN apt-get update && apt-get install -y iputils-ping
RUN apt-get update && apt-get install -y python3-pip python-dev build-essential
RUN pip install validators

COPY . .


