# Generated by Django 3.0.1 on 2020-02-07 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0021_auto_20200207_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamer',
            name='platform',
            field=models.CharField(choices=[('Mixer', 'Mixer'), ('Twitch', 'Twitch'), ('Facebook', 'Facebook'), ('Youtube', 'Youtube')], max_length=30),
        ),
    ]
