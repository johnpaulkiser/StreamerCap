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
    # subscriber_count = models.IntegerField()

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username
    


class LiveSession(models.Model):
    streamer = models.ForeignKey(Streamer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    viewer_count = models.IntegerField(null=True, blank=True)
    # max_viewers = models.IntegerField()
    # avg_viewers = models.IntegerField()
    is_live = models.BooleanField()
    rank = models.IntegerField(null=True, blank=True)
    
    #start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True) 
    

    @property
    def stream_link(self):

        return f'https://{self.streamer.platform}.com/{self.streamer}'

    
    def set_viewer_count(self):
        ''' sets the most recent viewership '''
        self.viewer_count = Viewership.objects.filter(
            live_session=self
            )[0].viewer_count




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
    