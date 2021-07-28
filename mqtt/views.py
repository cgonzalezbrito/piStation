from django.shortcuts import render
from django.http import HttpResponse

from .models import Broker, Location, PhysicalVar, Topic, Field, Fields

from . import tasks

def index(request):
    """View function for home page"""

    broker_host = Broker.objects.first()
    broker_port = Broker.objects.first().broker_port
    client_id = Broker.objects.first().client_id

    context = {
            'broker_host':broker_host,
            'broker_port':broker_port,
            'client_id':client_id,
            }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

#Method specified by url with ajax
def toggle_mqtt_status(req):
    status = Broker.objects.first().status
    if req.method == 'GET':
        if status:
            tasks.mqtt_stop()
            Broker.objects.first().status = False
        else:
            tasks.mqtt_start()
            Broker.objects.first().status = True

        # write_data.py write_csv()Call the method.
        #Of the data sent by ajax"input_data"To get by specifying.
        #write_data.write_csv(req.GET.get("input_data"))
        return HttpResponse()
