from django.db import models

# Create your models here.

platforms = {
    ('Twitch', 'Twitch'),
    ('Youtube', 'Youtube'),
    ('Mixer', 'Mixer'),
    ('Facebook', 'Facebook'),
}

class Streamer(models.Model):
    username = models.CharField(unique=True, max_length=50)
    platform = models.CharField(max_length=30, choices=platforms)
    subscriber_count = models.IntegerField()

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username
    

class LiveSession(models.Model):
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    max_viewers = models.IntegerField()
    avg_viewers = models.IntegerField()
    is_live = models.BooleanField()
    current_viewers = models.IntegerField()
    rank = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f'{self.streamer} streamed from {self.start_time} to {self.end_time}'
