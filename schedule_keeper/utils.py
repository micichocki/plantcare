import os
import django
from datetime import date, timedelta
from django.contrib.auth.models import User
from .models import Category, Plant, WateringSchedule, Post, Follow
from plantcare import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plantcare.settings')
django.setup()
settings.configure()


def load_data():
    # Create categories
    category1 = Category.objects.create(name='Indoor Plants')
    category2 = Category.objects.create(name='Outdoor Plants')

    # Create plants
    plant1 = Plant.objects.create(name='Snake Plant', description='A popular indoor plant with low maintenance.',
                                  category=category1, watering_frequency=14)
    plant2 = Plant.objects.create(name='Rose Bush',
                                  description='An outdoor flowering plant that requires regular sunlight.',
                                  category=category2, watering_frequency=7)

    # Create watering schedules
    watering_schedule1 = WateringSchedule.objects.create(plant=plant1, last_watered=date.today() - timedelta(days=5),
                                                         next_watering_date=date.today() + timedelta(days=9))
    watering_schedule2 = WateringSchedule.objects.create(plant=plant2, last_watered=date.today() - timedelta(days=3),
                                                         next_watering_date=date.today() + timedelta(days=4))

    # Create users
    user1 = User.objects.create(username='plantlover1', password='password1')
    user2 = User.objects.create(username='gardenenthusiast2', password='password2')

    # Create posts
    post1 = Post.objects.create(user=user1, plant=plant1, content='Just repotted my snake plant! #PlantCare',
                                img='path/to/image_snake_plant.jpg')
    post2 = Post.objects.create(user=user2, plant=plant2, content='Admiring the beautiful roses in my garden. 🌹',
                                img='path/to/image_rose_bush.jpg')

    # Create follows
    follow1 = Follow.objects.create(user=user1, plant=plant2)
    follow2 = Follow.objects.create(user=user2, plant=plant1)

    print('Data loaded successfully.')


if __name__ == "__main__":
    load_data()
