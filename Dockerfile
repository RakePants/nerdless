FROM python

RUN mkdir -p /home/app
RUN python -m pip install transformers[torch]
RUN python -m pip install aiogram

COPY ./app /home/app

CMD ["python", "/home/app/bot/bot.py"]