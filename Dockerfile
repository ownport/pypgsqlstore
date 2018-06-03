FROM alpine:3.7

RUN apk add --no-cache \
        make \
        python3 \
        postgresql-dev && \
    apk add --no-cache --virtual .build-deps \
        gcc \
        python3-dev \
        musl-dev \
        build-base && \
    pip3 install --upgrade \
        pip \
        setuptools && \
    pip3 install \
        pytest \
        pytest-cov \
        pytest-mock \
        pytest-xdist \
        pytest-benchmark \
        psycopg2-binary==2.7.4 && \
    apk del .build-deps

