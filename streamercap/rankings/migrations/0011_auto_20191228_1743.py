# Generated by Django 3.0.1 on 2019-12-28 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0010_livesession_viewer_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livesession',
            name='viewer_count',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='streamer',
            name='platform',
            field=models.CharField(choices=[('Mixer', 'Mixer'), ('Facebook', 'Facebook'), ('Twitch', 'Twitch'), ('Youtube', 'Youtube')], max_length=30),
        ),
    ]