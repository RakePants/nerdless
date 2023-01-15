FROM python

RUN mkdir -p /home/app
RUN python -m pip install transformers
RUN python -m pip install aiogram

COPY . /home/app

CMD ["python", "/home/app/bot/bot.py"]