# Generated by Django 2.2.4 on 2019-09-12 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corus', '0037_auto_20190912_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='company',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='complain',
            name='m_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='complain',
            name='cdate',
            field=models.DateField(default=datetime.datetime(2019, 9, 12, 21, 38, 48, 895954)),
        ),
        migrations.AlterField(
            model_name='item',
            name='idate',
            field=models.DateField(default=datetime.datetime(2019, 9, 12, 21, 38, 48, 880331)),
        ),
        migrations.AlterField(
            model_name='order',
            name='odate',
            field=models.DateField(default=datetime.datetime(2019, 9, 12, 21, 38, 48, 895954)),
        ),
        migrations.AlterField(
            model_name='transection',
            name='tdate',
            field=models.DateField(default=datetime.datetime(2019, 9, 12, 21, 38, 48, 895954)),
        ),
    ]
