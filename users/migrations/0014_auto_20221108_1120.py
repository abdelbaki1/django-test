# Generated by Django 3.1.3 on 2022-11-08 11:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20221108_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_activity',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
