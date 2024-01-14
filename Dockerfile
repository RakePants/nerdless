FROM python:3.11.4-slim

RUN echo $(python3 -m site --user-base)

COPY requirements.txt  .

ENV PATH /home/root/.local/bin:${PATH}
ENV PYTHONPATH=/usr/src

RUN apt-get update && pip install --upgrade pip && pip install -r requirements.txt  

COPY . .

CMD python -m app.main