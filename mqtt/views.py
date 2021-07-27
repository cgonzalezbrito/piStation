from django.shortcuts import render

from .models import Broker, Location, PhysicalVar, Topic, Field, Fields

def index(request):
    """View function for home page"""

    context = {
            'broker_host':Broker.broker_host,
            'broker_port':Broker.broker_port,
            'client_id':Broker.client_id,
            }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
