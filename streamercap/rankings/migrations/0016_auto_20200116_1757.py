# Generated by Django 3.0.1 on 2020-01-16 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0015_auto_20200113_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamer',
            name='platform',
            field=models.CharField(choices=[('Mixer', 'Mixer'), ('Twitch', 'Twitch'), ('Facebook', 'Facebook'), ('Youtube', 'Youtube')], max_length=30),
        ),
    ]