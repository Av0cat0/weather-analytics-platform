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
- OpenWeatherMap API key
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

### 6. Health Checks

```bash
# Check Elasticsearch
curl http://localhost:9200/_cluster/health?pretty

# Check weather data
curl "http://localhost:9200/weather-*/_search?pretty&size=1&sort=@timestamp:desc"

# Check RabbitMQ
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

The system includes **automatic alerts** that are **pre-configured** and ready to use:

- **❄️ Low Temperature Alert**: Automatically triggers when temperature drops below **0°C**
- **🔥 High Temperature Alert**: Automatically triggers when temperature rises above **24°C**

**Alert Features:**
- ✅ **Pre-configured**: Alerts are already set up in the system
- ✅ **Automatic**: No manual setup required
- ✅ **Real-time**: Evaluates every minute
- ✅ **Visual**: Appears in Grafana dashboard
- ✅ **Detailed**: Shows current temperature and threshold information

**Alert Configuration:**
- **Evaluation Frequency**: Every 1 minute
- **Alert Conditions**: 
  - Temperature < 0°C (Low alert)
  - Temperature > 24°C (High alert)
- **Alert State**: Shows in Grafana Alerting section

## Data Monitoring

The dashboard displays:

- 📊 Temperature graph over time
- 💧 Humidity graph
- 🌬️ Wind speed graph
- 📈 Atmospheric pressure graph
- 📱 Current statistics
- ⏰ Precise sampling time at millisecond level

## Troubleshooting

### Common Issues

1. **Application not connecting to RabbitMQ**
   ```bash
   docker-compose logs weather_monitor
   ```

2. **Data not appearing in Grafana**
   ```bash
   # Check Elasticsearch
   curl http://localhost:9200/weather-*/_search?pretty
   
   # Check Logstash
   docker-compose logs logstash
   ```

3. **API key not working**
   - Verify the key is correct
   - Check that the key is active in OpenWeatherMap

### Logs

```bash
# View logs for all services
docker-compose logs -f

# Logs for specific service
docker-compose logs -f weather_monitor
docker-compose logs -f logstash
docker-compose logs -f grafana
```

## Development

### Local Running

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python weather_monitor.py
```


## License

MIT License

## Contributing

1. Fork the project
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you have questions or issues, open an issue in the GitHub repository.