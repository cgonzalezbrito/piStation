# Create your tasks here

from celery import shared_task

@shared_task
def test():
    print('IS WORKING')

