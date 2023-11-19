# Generated by Django 4.2.7 on 2023-11-12 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('watering_frequency', models.PositiveIntegerField(help_text='Watering frequency in days')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule_keeper.category')),
            ],
        ),
        migrations.CreateModel(
            name='WateringSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_watered', models.DateField()),
                ('next_watering_date', models.DateField()),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule_keeper.plant')),
            ],
        ),
    ]