# Weather Monitoring System

Complete weather monitoring system with OpenWeatherMap API, RabbitMQ, Elasticsearch, Logstash, Grafana, and Jenkins.

## Features

-  Weather sampling every hour from OpenWeatherMap API
-  Data sending to RabbitMQ
-  Data flow through Logstash to Elasticsearch
-  Grafana dashboard with alerts
-  CI/CD Pipeline with Jenkins
-  Everything ready for Docker Compose
-  Automatic temperature alerts

## Requirements

- Docker & Docker Compose
- Git

## Installation and Setup

### 1. Environment Variables Setup

Set the city to sample its weather in .env file:
```
CITY_NAME=Rome
```

### 2. Running the System

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f weather_monitor
docker-compose logs -f logstash
docker-compose logs -f grafana

# Stop the system
docker-compose down

# Shutdown with volume deletion
docker-compose down -v
```

### 3. Service Access

- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **Elasticsearch**: http://localhost:9200
- **Jenkins**: http://localhost:8080

### 4. Health Checks

```bash
# Check Elasticsearch
curl http://localhost:9200/_cluster/health?pretty

# Check weather data
curl "http://localhost:9200/weather-*/_search?pretty&size=1&sort=@timestamp:desc"

# Check RabbitMQ
Invoke-WebRequest -Uri "http://localhost:15672/api/queues" -Headers @{"Authorization"="Basic Z3Vlc3Q6Z3Vlc3Q="}
```

**Note:** When checking health for RabbitMQ on a different OS than Windows, you can use this command:
```bash
curl -u guest:guest http://localhost:15672/api/queues
```

## Project Structure

```
├── weather_monitor.py          # Main Python application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image for application
├── docker-compose.yml          # All services configuration
├── logstash.conf              # Logstash configuration
├── weather_template.json       # Elasticsearch template
├── Jenkinsfile                # CI/CD Pipeline
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/       # Elasticsearch configuration
│   │   └── dashboards/        # Dashboard configuration
│   └── dashboards/
│       └── weather-dashboard.json
└── README.md
```

## CI/CD Pipeline

The Pipeline includes:

1. **Clone** - Code cloning
2. **Build** - Docker image building
3. **Deploy** - Production deployment
4. **Notify Success** - Success notification

## Grafana Alerts

The system includes **automatic alerts** that are **pre-configured** and ready to use.
The alert automatically triggers when temperature drops below **0°C** or rises above **24°C**
The alert state shows as the color of the dot, if it's in alert state it will be colored red, otherwise green.
