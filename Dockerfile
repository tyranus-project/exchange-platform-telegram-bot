# FROM python:3.8-slim-buster
FROM python:3.9-slim

WORKDIR /exchange-platform-telegram-bot

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app /exchange-platform-telegram-bot/app

CMD ["python", "-m", "app"]