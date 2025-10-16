FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY weather_monitor.py .

RUN useradd -m -u 1000 weatheruser && chown -R weatheruser:weatheruser /app
USER weatheruser

ENV PYTHONUNBUFFERED=1

CMD ["python", "weather_monitor.py"]

