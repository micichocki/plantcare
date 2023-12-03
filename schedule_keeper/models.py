import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Plant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    watering_frequency = models.PositiveIntegerField(help_text="Watering frequency in days")
    img = models.ImageField(upload_to="uploads/% Y/% m/% d/", null=True)

    def __str__(self):
        return self.name


class WateringSchedule(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    last_watered = models.DateField()
    next_watering_date = models.DateField()

    def __str__(self):
        return f"{self.plant.name} - Last Watered: {self.last_watered}, Next Watering: {self.next_watering_date}"


def upload_to(instance, filename):
    now = timezone.now()
    upload_path = os.path.join('static', 'uploads', str(now.year), str(now.month), str(now.day))
    return os.path.join(upload_path, filename)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    content = models.TextField()
    img = models.ImageField(upload_to=upload_to, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plant.name} - {self.created_at}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} follows {self.plant.name}"

    def is_following(self, user, plant):
        return Follow.objects.filter(user=user, plant=plant).exists()
