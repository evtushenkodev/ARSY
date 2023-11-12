FROM ubuntu:20.04

LABEL maintainer="Max <evtushenkodev@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /web

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    libpq-dev \
    gcc \
    python3-dev \
    build-essential \
    libpcre3-dev \
    blender

COPY requirements.txt /web
RUN pip3 install -r requirements.txt

COPY . /web

RUN pip3 install uwsgi

RUN chmod +x /web/entrypoint.sh

ENTRYPOINT ["/web/entrypoint.sh"]
