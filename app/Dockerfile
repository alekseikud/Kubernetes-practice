FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt &&\
    apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY app.py app.py

CMD ["python","app.py"]