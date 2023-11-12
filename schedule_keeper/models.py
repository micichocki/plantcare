# models.py

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Plant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    watering_frequency = models.PositiveIntegerField(help_text="Watering frequency in days")

    def __str__(self):
        return self.name


class WateringSchedule(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    last_watered = models.DateField()
    next_watering_date = models.DateField()

    def __str__(self):
        return f"{self.plant.name} - Last Watered: {self.last_watered}, Next Watering: {self.next_watering_date}"
