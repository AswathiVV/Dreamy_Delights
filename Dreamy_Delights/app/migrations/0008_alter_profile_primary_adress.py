# Generated by Django 5.1.2 on 2025-02-21 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='primary_adress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.address'),
        ),
    ]
