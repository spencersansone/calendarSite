# Generated by Django 2.0.3 on 2018-09-11 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180911_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('datetime_created', models.DateTimeField()),
                ('completed', models.BooleanField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Event')),
            ],
        ),
    ]
