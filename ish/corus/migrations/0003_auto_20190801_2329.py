# Generated by Django 2.2.3 on 2019-08-01 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corus', '0002_auto_20190801_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eregiser',
            name='email',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='head',
            name='email',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='uregiser',
            name='email',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]