# Generated by Django 2.0.3 on 2018-04-10 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20180410_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='partograph',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
