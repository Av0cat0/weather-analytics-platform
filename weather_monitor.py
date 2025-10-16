#!/usr/bin/env python3
"""
Weather Monitor Application
Monitors weather data from OpenWeatherMap API and sends to RabbitMQ
"""

import os
import time
import json
import logging
import requests
import pika
from datetime import datetime
from typing import Dict, Any
import schedule

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WeatherMonitor:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
        self.city = os.getenv('CITY_NAME', 'Tel Aviv')  # Default to Tel Aviv
        self.rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        self.rabbitmq_port = int(os.getenv('RABBITMQ_PORT', '5672'))
        self.queue_name = os.getenv('QUEUE_NAME', 'weather_data')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def send_to_rabbitmq(self, data: Dict[str, Any]):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.rabbitmq_host, port=self.rabbitmq_port)
            )
            channel = connection.channel()
            
            # Declare the queue
            channel.queue_declare(queue=self.queue_name, durable=True)
            
            # Publish the message
            message = json.dumps(data, ensure_ascii=False)
            channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            
            connection.close()
            print(f"Data sent to RabbitMQ")
            
        except Exception as e:
            logger.error(f"Failed to send data to RabbitMQ: {e}")
            raise
    
    def get_weather_data(self) -> Dict[str, Any]:
        try:
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric'  # Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            weather_data = {
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'timestamp_ms': int(time.time() * 1000),  # Millisecond precision
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'weather_main': data['weather'][0]['main'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 0),
                'cloudiness': data['clouds']['all'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat() + 'Z',
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat() + 'Z',
                'coord_lat': data['coord']['lat'],
                'coord_lon': data['coord']['lon']
            }
            
            print(f"Weather: {self.city} {weather_data['temperature']}°C")
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except KeyError as e:
            logger.error(f"Unexpected API response format: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching weather data: {e}")
            raise
    
    
    def check_temperature_alerts(self, temperature: float):
        """Check temperature against alert thresholds"""
        if temperature < 0:
            print(f"ALERT: Temperature is {temperature}°C - BELOW 0°C!")
        elif temperature > 24:
            print(f"ALERT: Temperature is {temperature}°C - ABOVE 24°C!")
        else:
            print(f"Temperature {temperature}°C is within normal range (0-24°C)")
    
    def collect_and_send_weather(self):
        """Main function to collect weather data and send to RabbitMQ"""
        try:
            weather_data = self.get_weather_data()
            self.check_temperature_alerts(weather_data['temperature'])
            self.send_to_rabbitmq(weather_data)
            
        except Exception as e:
            logger.error(f"Weather data collection failed: {e}")
    
    def start_monitoring(self):
        """Start the weather monitoring service"""
        print(f"Monitoring {self.city} every hour")
        
        # Schedule weather collection every hour
        schedule.every().hour.do(self.collect_and_send_weather)
        
        # Run immediately on start
        self.collect_and_send_weather()
        
        # Keep the service running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("Stopped")
        finally:
            pass

def main():
    monitor = WeatherMonitor()
    monitor.start_monitoring()

if __name__ == "__main__":
    main()

