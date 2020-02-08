import json
import requests
from .models import Streamer, LiveSession, Viewership
from .twitch_service import set_streams_offline


def make_request(num=100):
    '''can get a max of 100 streams per request '''

    URL = f'https://mixer.com/api/v1/channels?order=viewersCurrent:desc,limit={num}'
    r = requests.get(url=URL)
    return r.json()


def get_top_streams():

    online_streams = set()
    while True:

        streams = make_request()
        for stream in streams:
            if stream["viewersCurrent"] < 100:
                set_streams_offline(online_streams, 'Mixer')
                print(f'Finished Querying {len(online_streams)} streams from Mixer')
                return

            id = streams_to_db(stream)
            online_streams.add(id)
            

def streams_to_db(stream):
    
    
    streamer, created = Streamer.objects.get_or_create(
        username=stream['token'],
        platform='Mixer'
    )
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

    if stream['languageId'] == None:
        session.language = "en"
    else:
        session.language = stream['languageId']
    
    Viewership.objects.create(
        live_session = session,
        viewer_count = stream['viewersCurrent']
    )
    session.set_viewer_count()
    session.save()
    
    return streamer.id
    


