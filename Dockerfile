FROM alpine:3.5
MAINTAINER Lei Zhang <antiagainst@gmail.com>

ADD repositories /etc/apk/repositories

RUN apk --update add --no-cache --upgrade cppcheck@community python3 py3-lxml@main

RUN adduser -u 9000 -D -s /bin/false app
USER app

COPY . /usr/src/app

VOLUME /code
WORKDIR /code

CMD ["python3", "/usr/src/app/codeclimate-cppcheck.py"]
