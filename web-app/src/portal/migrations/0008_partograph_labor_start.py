# Generated by Django 2.0.3 on 2018-07-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20180630_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='partograph',
            name='labor_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
