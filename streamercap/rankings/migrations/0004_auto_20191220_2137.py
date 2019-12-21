# Generated by Django 3.0.1 on 2019-12-20 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0003_auto_20191220_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livesession',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='streamer',
            name='platform',
            field=models.CharField(choices=[('Facebook', 'Facebook'), ('Youtube', 'Youtube'), ('Twitch', 'Twitch'), ('Mixer', 'Mixer')], max_length=30),
        ),
    ]
