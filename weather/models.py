from django.db import models

class WeatherData(models.Model):
    location = models.CharField(max_length=255)
    date = models.DateField()
    temperature = models.FloatField()

    def __str__(self):
        return f"{self.location} - {self.date} - {self.temperature}°F"
