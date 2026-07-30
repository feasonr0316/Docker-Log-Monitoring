FROM python:3.10-slim

WORKDIR /app/collector

COPY collector/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY collector /app/collector

CMD ["python", "collector.py"]

