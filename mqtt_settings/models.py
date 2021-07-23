from django.db import models

class Field(models.Model):
    """Model field"""
    name = models.CharField(max_lengh=200, help_text='Enter field type')

    def __str__(self):
        """String for field"""
        return self.name
