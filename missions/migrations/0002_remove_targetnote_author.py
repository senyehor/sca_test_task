# Generated by Django 5.1.3 on 2024-11-19 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='targetnote',
            name='author',
        ),
    ]
