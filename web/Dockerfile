FROM ubuntu:23.10

LABEL maintainer="Max <evtushenkodev@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /web

RUN apt-get update --fix-missing && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    gcc \
    libpq-dev \
    build-essential \
    libpcre3-dev \
    blender \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /web
RUN pip3 install -r requirements.txt

COPY . /web

RUN pip3 install uwsgi

RUN chmod +x /web/entrypoint.sh

ENTRYPOINT ["/web/entrypoint.sh"]
