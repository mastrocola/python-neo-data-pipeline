FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install --assume-yes --no-install-recommends -qq \
    build-essential \
    software-properties-common \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  pip install --quiet --upgrade pip --no-cache-dir && \
  pip install --quiet -r requirements.txt --no-cache-dir

COPY . .

CMD celery -A src.app.celery worker --beat --loglevel=info --concurrency=4 --without-heartbeat
