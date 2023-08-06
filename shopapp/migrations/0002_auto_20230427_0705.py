# Generated by Django 3.2.13 on 2023-04-27 07:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='userid',
            field=models.CharField(default=uuid.uuid4, max_length=36),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
