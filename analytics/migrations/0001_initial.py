# Generated by Django 4.0.3 on 2022-03-28 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('short_urls', '0002_shorturl_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortUrlVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurred', models.DateTimeField()),
                ('short_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='short_urls.shorturl')),
            ],
        ),
        migrations.AddIndex(
            model_name='shorturlvisit',
            index=models.Index(fields=['occurred'], name='analytics_s_occurre_8d0278_idx'),
        ),
    ]
