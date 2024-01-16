FROM python:3.11.4-slim

WORKDIR /usr/src/

ENV PYTHONPATH=/usr/src

COPY requirements.txt ./app/

RUN apt-get update && pip install --upgrade pip && pip install -r ./app/requirements.txt  

COPY . ./app/

CMD ["python", "app/main.py"]