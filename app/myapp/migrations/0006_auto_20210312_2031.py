# Generated by Django 3.1.7 on 2021-03-12 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_animal'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='car',
            unique_together={('make', 'model')},
        ),
    ]