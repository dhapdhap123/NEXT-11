# Generated by Django 4.1.7 on 2023-03-31 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_article_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='date',
        ),
    ]
