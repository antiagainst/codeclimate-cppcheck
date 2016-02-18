FROM alpine
MAINTAINER antiagainst

ADD repositories /etc/apk/repositories

RUN apk --update add cppcheck@testing python py-lxml

RUN adduser -u 9000 -D -s /bin/false app
USER app

COPY . /usr/src/app

VOLUME /code
WORKDIR /code

CMD ["python", "/usr/src/app/codeclimate-cppcheck.py"]
