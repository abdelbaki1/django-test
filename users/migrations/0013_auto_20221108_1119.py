# Generated by Django 3.1.3 on 2022-11-08 11:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_activity_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_activity',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 8, 11, 18, 59, 487992, tzinfo=utc)),
        ),
    ]
