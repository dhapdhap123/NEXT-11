# Generated by Django 4.1.7 on 2023-03-31 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_article_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
