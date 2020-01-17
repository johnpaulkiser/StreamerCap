import json
import requests
from .models import Streamer, LiveSession, Viewership
from .twitch_service import set_streams_offline


def get_top_streams(num=100):
    '''can get a max of 100 streams per request '''

    URL = f'https://mixer.com/api/v1/channels?order=viewersCurrent:desc,limit={num}'
    r = requests.get(url=URL)
    return r.json()


def streams_to_db(num=100):
    
    online_streamers = set()

    streams = get_top_streams(num)
    print(json.dumps(streams, indent=2))
    for stream in streams:
        
        
        streamer, created = Streamer.objects.get_or_create(
            username=stream['token'],
            platform='Mixer'
        )
        online_streamers.add(streamer)
        try:
            game_title = stream['type']['name']
        except KeyError:
            game_title = "No Game Title"
       
        
            

        session, created = LiveSession.objects.get_or_create(
            streamer=streamer,
            is_live=True,
        )
        session.title = stream['name']
        session.game = game_title
        
        Viewership.objects.create(
            live_session = session,
            viewer_count = stream['viewersCurrent']
        )
        session.set_viewer_count()
        session.save()
        
    set_streams_offline(online_streamers, 'Mixer')
    

