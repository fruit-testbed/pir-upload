FROM alpine:latest
MAINTAINER Tony Garnock-Jones <tonyg@leastfixedpoint.com>

RUN \
    apk --no-cache --no-progress upgrade && \
    apk --no-cache --no-progress add python3 py3-pip && \
    apk --no-cache --no-progress add python3-dev libc-dev gcc && \
    pip3 install RPi.GPIO mini-syndicate

COPY *.py /

ENTRYPOINT ["/usr/bin/python3", "/pir-upload.py"]
