# Generated by Django 3.2.2 on 2021-05-19 07:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210519_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]