# Generated by Django 4.2 on 2023-04-13 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_remove_comment_parent_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recomment',
            name='parent_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.comment'),
        ),
    ]