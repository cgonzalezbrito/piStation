from django.shortcuts import render
from django.http import HttpResponse

from .models import Broker, Location, PhysicalVar, Topic, Field, Fields

from . import tasks

import os
from piStation import celery

def index(request):
    """View function for home page"""

    data = []
    for obj in Broker.objects.all():
        
        data.append({
            'broker_host':obj,
            'broker_port':obj.broker_port,
            'client_id':obj.client_id,
            'uuid': obj.uuid
            })

    context = { 'data': data }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

#Method specified by url with ajax
def toggle_mqtt_status(req):
    qs = Broker.objects.filter(uuid=req.GET.get("input_data"))
    status = qs[0].status
    if req.method == 'GET':
        if status:
            tasks.mqtt_stop()
            qs.update(status=False)
        else:
            tasks.mqtt_start(req.GET.get("input_data"))
            qs.update(status=True)
            celery.app.worker_main(argv=['worker','--loglevel=info'])

        return HttpResponse()
