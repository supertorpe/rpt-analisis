FROM python:3.13.0-slim

RUN rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip &&\
    chmod -R 777 /opt/venv

COPY ./docker/requirements.txt /tmp/requirements.txt
RUN /opt/venv/bin/pip install -r /tmp/requirements.txt &&\
    rm /tmp/requirements.txt

COPY ./docker/startup.sh /

WORKDIR /app

ENTRYPOINT ["/startup.sh"]