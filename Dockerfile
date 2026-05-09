FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY snmp_collector.py .

EXPOSE 8000
CMD ["python", "snmp_collector.py"]
