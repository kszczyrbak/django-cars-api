# Generated by Django 3.1.5 on 2021-02-13 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]