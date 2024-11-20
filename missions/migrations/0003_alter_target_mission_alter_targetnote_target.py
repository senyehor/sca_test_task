# Generated by Django 5.1.3 on 2024-11-20 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0002_remove_targetnote_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='mission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='missions.mission'),
        ),
        migrations.AlterField(
            model_name='targetnote',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='missions.target'),
        ),
    ]
