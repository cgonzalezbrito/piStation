from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        #Add the following(views.py call_write_data()Allows you to send data to)
        path("ajax/", views.toggle_mqtt_status, name="toggle_mqtt_status"),
]

