# Generated by Django 3.2.5 on 2021-07-20 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_time_escudo'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=100, verbose_name='Slug'),
        ),
    ]
