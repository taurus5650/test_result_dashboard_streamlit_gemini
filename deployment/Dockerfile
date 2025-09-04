FROM python:3.13-slim

ENV TZ=Asia/Taipei

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

