# Generated by Django 2.0.3 on 2018-09-11 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_evententry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evententry',
            name='event',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='EventEntry',
        ),
    ]
