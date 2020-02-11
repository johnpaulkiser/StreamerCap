from django.db import models

# Create your models here.

platforms = {
    ('Twitch', 'Twitch'),
    ('Youtube', 'Youtube'),
    ('Mixer', 'Mixer'),
    ('Facebook', 'Facebook'),
}


class Streamer(models.Model):
    username = models.CharField(unique=False, max_length=50)
    platform = models.CharField(max_length=30, choices=platforms)
    # subscriber_count = models.IntegerField()

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username
    


class LiveSession(models.Model):
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    viewer_count = models.IntegerField(null=True, blank=True)
    game = models.CharField(max_length=200)
    language = models.CharField(max_length=10, default='en')
    is_live = models.BooleanField()
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delta_time = models.FloatField(default=1)
    
    
    @property
    def stream_link(self):
        return f'https://{self.streamer.platform}.com/{self.streamer}'


    def save(self, update_delta_time=False, *args, **kwargs):
        if update_delta_time:
            self.delta_time = (self.updated_at - self.started_at).total_seconds()
        super(LiveSession, self).save(*args, **kwargs)
    

    def set_viewer_count(self):
        ''' sets the most recent viewership '''

        self.viewer_count = Viewership.objects.filter(
            live_session=self
            )[0].viewer_count


    def as_dict(self):
        return {
            "rank": "null",
            "streamer": self.streamer.__str__(),
            "viewership": self.viewer_count,
            "category": self.game,
            "platform": self.streamer.platform,
            "title": self.title
        }


    def __str__(self):
        return f'{self.streamer} - {self.title}'



class Viewership(models.Model):
    live_session = models.ForeignKey(LiveSession, on_delete=models.CASCADE)
    viewer_count = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f'{self.live_session.streamer} -- {self.time} -- {self.viewer_count}'
    
