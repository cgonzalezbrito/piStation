# IoT Raspberry pi mqtt django device
Open source django based iot device. Web Interface Brokers configuration. Celery thread triggers of acquiring and publishing data. 

## Setup

Create and activate a python enviroment: 

  python3 -m venv .env  
  soruce .env/bin/activate

## Use

Exec thread

  celery -A piStation beat -l info
  celery -A piStation worker -l info
