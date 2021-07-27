# Create your tasks here

from celery import shared_task
from piStation.celery import app

@app.task
@shared_task
def test():
    print('IS WORKING')

