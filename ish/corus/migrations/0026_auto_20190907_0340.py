# Generated by Django 2.2.4 on 2019-09-06 22:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corus', '0025_auto_20190907_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='landmark',
            field=models.CharField(default='Your Address', max_length=300),
        ),
        migrations.AlterField(
            model_name='order',
            name='odate',
            field=models.DateField(default=datetime.datetime(2019, 9, 7, 3, 40, 24, 555296)),
        ),
    ]