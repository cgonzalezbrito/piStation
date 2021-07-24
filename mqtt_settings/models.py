from django.db import models

class Broker(models.Model):
    """Model Broker"""
    broker_host = models.CharField(
            max_length = 200,
            unique = True, 
            )
    broker_port = models.IntegerField(
            default = 1883,
            help_text = 'default: 1883',
            )
    description = models.TextField(
            blank = True,
            help_text = 'Optional broker description',
            )

    def Host(self):
        """Return broker host"""
        return self.broker_host

    def Port(self):
        """Return broker port"""
        return self.broker_port

class Client(models.Model):
    """Model Client"""
    client_id = models.CharField(
            max_length = 200,
            )

    def __str__(self):
        """String for Client"""
        return self.client_id

class Location(models.Model):
    """Location"""
    place = models.CharField(
            max_length = 200,
            help_text = 'The topic of the device is PLACE_LOCATION/PHYSICAL_VARIABLE'
            )
    location = models.CharField(
            max_length = 200,
            help_text = 'The topic of the device is PLACE_LOCATION/PHYSICAL_VARIABLE'
            )

    def __str__(self):
        """String for Location"""
        return f'{self.place},{self.location}'

class PhysicalVar(models.Model):
    """Temp, pressure, volts, etc"""
    name = models.CharField(
            max_length = 200,
            help_text = 'temp, pressure, volts, etc',
            )
    unit = models.CharField(
            max_length = 10,
            )

    def __str__(self):
        """String for PhysicalVar"""
        return self.name

class Topic(models.Model):
    """Topic"""
    location = models.ForeignKey(
            'Location',
            on_delete = models.SET_NULL,
            null = True,
            )
    physical_variable = models.ForeignKey(
            'PhysicalVar',
            on_delete = models.SET_NULL,
            null = True,
            )

    def __str__(self):
        """String for Topic"""
        return f'{self.location},{self.physical_variable}'

class Field(models.Model):
    """Model field"""
    name = models.CharField(
            max_length=200,
            help_text='Enter field type'
            )

    def __str__(self):
        """String for field"""
        return self.name

class Fields(models.Model):
    """Fields = topic + field"""
    Topic = models.ForeignKey(
            'Topic',
            on_delete = models.SET_NULL,
            null = True,
            )

