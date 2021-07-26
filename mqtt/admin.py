from django.contrib import admin
from .models import Broker, Client, Fields, Field, Topic, Location, PhysicalVar

admin.site.register(Broker)
admin.site.register(Client)
admin.site.register(Fields)
admin.site.register(Field)
admin.site.register(Topic)
admin.site.register(Location)
admin.site.register(PhysicalVar)
