# Generated by Django 3.1.7 on 2021-03-13 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20210312_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='rates_sum',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
