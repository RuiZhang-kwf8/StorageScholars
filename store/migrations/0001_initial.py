# Generated by Django 5.0.2 on 2024-03-03 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(max_length=200)),
                ('mapID', models.TextField(max_length=200)),
                ('user', models.TextField(max_length=200)),
            ],
        ),
    ]
