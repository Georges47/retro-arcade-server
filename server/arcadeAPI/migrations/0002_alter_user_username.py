# Generated by Django 3.2.8 on 2021-11-13 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arcadeAPI', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
