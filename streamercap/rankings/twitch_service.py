import os
import requests
import json
from datetime import datetime
from .models import Streamer, LiveSession, Viewership
from streamercap.settings import DEBUG

if DEBUG:
    config_location = 'config.json'
else:
    config_location = '/etc/config.json'

with open(config_location) as config_file:
    config = json.load(config_file)



def get_top_streams(num=1000):
    URL = f'https://api.twitch.tv/helix/streams?first={num}'
    headers = {'Client-ID': config['TWITCH_ID']}
    r = requests.get(url=URL, headers=headers)
    return r.json()



def get_streamer_usernames(num=10):

    streamer_list = get_top_streams(num)["data"]
    return [streamer["user_name"] for streamer in streamer_list]




def streams_to_db(num=100):
    
    online_titles = set()
    streams = get_top_streams(num)
    print(streams)
    for stream in streams["data"]:
        title = stream["title"]
        online_titles.add(title)
        streamer, created = Streamer.objects.get_or_create(
            username=stream["user_name"],
            platform="Twitch"
        )
        session, created = LiveSession.objects.get_or_create(
            streamer=streamer,
            title=title,
            is_live=True,
            #start_time=datetime.now()
        )
        Viewership.objects.create(
            live_session = session,
            viewer_count = stream["viewer_count"]
        )
        session.set_viewer_count()
        session.save()
    
    set_streams_offline(online_titles)


def set_streams_offline(online_titles):
    offline_streams = LiveSession.objects.filter(is_live=True).exclude(title__in=online_titles)       
        
    for stream in offline_streams:
        stream.is_live = False
        stream.save()






# if __name__ == "__main__":
#     # print(get_streamer_usernames())
#     print(json.dumps(get_top_streams(1), indent=4))
