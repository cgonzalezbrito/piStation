from django.shortcuts import render

from .models import Broker, Location, PhysicalVar, Topic, Field, Fields

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
