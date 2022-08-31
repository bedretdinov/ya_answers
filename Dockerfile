FROM python:3.6

LABEL maintainer="mlbox"

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
WORKDIR /app
ENV PYTHONUNBUFFERED 1
COPY . /app

RUN set -e; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        software-properties-common \
    ; \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9; \
    apt-add-repository 'deb http://repos.azulsystems.com/debian stable main'; \
    apt-get update; \
    apt-get clean; \
    rm -rf /var/tmp/* /tmp/* /var/lib/apt/lists/*

RUN echo "PWD is: $PWD"
RUN  pip install --upgrade pip \
&&   pip install -r requirements.txt


