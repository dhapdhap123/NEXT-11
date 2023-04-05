# Generated by Django 4.1.7 on 2023-03-31 05:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_article_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False, verbose_name='date published'),
        ),
    ]