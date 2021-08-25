# IoT Raspberry pi mqtt django device
Open source django based iot device. Web Interface Brokers configuration. Celery thread triggers of acquiring and publishing data. 

## Setup

Create and activate a python enviroment: 

  apt-get install python3-venv

  python3 -m venv .env  
  soruce .env/bin/activate
  
  pip install django -U
  pip install -r requirements.txt

## Use

Exec thread

  celery -A piStation beat -l info
  celery -A piStation worker -l info
