# Generated by Django 4.0.3 on 2022-03-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('short_urls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shorturl',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]