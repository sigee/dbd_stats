FROM python:3.10.2-slim

RUN apt-get -y update && \
    apt-get -y full-upgrade

COPY /src /app
RUN mkdir -p /data
WORKDIR /app

COPY requirements.txt requirements.txt
COPY run.sh run.sh

WORKDIR /app

RUN pip install --user --no-cache-dir -r requirements.txt

CMD ["./run.sh"]