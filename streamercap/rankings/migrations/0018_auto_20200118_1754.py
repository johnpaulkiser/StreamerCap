# Generated by Django 3.0.1 on 2020-01-18 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0017_auto_20200118_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamer',
            name='platform',
            field=models.CharField(choices=[('Youtube', 'Youtube'), ('Facebook', 'Facebook'), ('Twitch', 'Twitch'), ('Mixer', 'Mixer')], max_length=30),
        ),
    ]
