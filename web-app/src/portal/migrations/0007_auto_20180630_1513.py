# Generated by Django 2.0.3 on 2018-06-30 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20180417_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partomeasure',
            name='descent',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='partomeasure',
            name='station',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
