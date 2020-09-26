FROM python:3.8-alpine
RUN apk add --virtual .build-dependencies \ 
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            pcre-dev

ADD requirements.txt /
RUN pip install -r /requirements.txt