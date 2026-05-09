# Network Monitor

SNMP-based network telemetry collector with Prometheus and Grafana.

## Features

- Collects SNMP metrics from network devices:
  - CPU usage
  - Uptime
  - Interface traffic in/out
- Exposes metrics at `/metrics` for Prometheus scrape
- Includes baseline alert rules for high CPU and collector availability

## Stack

- Python (`pysnmp`, `prometheus-client`)
- Prometheus
- Grafana
- Docker Compose

## Run

```bash
docker compose up -d --build
```

Endpoints:

- Collector metrics: `http://localhost:8000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## Configure Target Device

Edit in `snmp_collector.py`:

- `DEVICE_IP`
- `COMMUNITY`

## Alerts

Rules in `prometheus/alerts.yml`:

- `DeviceCpuHigh`
- `CollectorDown`
