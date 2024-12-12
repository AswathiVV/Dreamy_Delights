# Generated by Django 5.1.2 on 2024-12-11 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CupCake',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('img', models.FileField(upload_to='')),
                ('category', models.TextField()),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LayerCake',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('img', models.FileField(upload_to='')),
                ('category', models.TextField()),
                ('colour', models.TextField()),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OneTierCake',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('img', models.FileField(upload_to='')),
                ('category', models.TextField()),
                ('colour', models.TextField()),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TwoTierCake',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('img', models.FileField(upload_to='')),
                ('category', models.TextField()),
                ('colour', models.TextField()),
                ('quantity', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
    ]
