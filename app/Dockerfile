FROM python:3.11.4-slim

RUN addgroup --gid 10001 appuser && \
    adduser --uid 10001 --gid 10001 --disabled-password --gecos "" appuser

WORKDIR /usr/src/

ENV PYTHONPATH=/usr/src

COPY requirements.txt ./app/

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r ./app/requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --chown=appuser:appuser . ./app/

USER appuser

CMD ["python", "app/main.py"]