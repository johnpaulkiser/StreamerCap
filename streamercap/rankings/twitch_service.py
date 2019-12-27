import os
import requests
import json
from datetime import datetime
from .models import Streamer, LiveSession, Viewership

def get_top_streams(num=1000):
    URL = f'https://api.twitch.tv/helix/streams?first={num}'
    headers = {'Client-ID': os.environ['TWITCH_ID']}
    r = requests.get(url=URL, headers=headers)
    return r.json()



def get_streamer_usernames(num=10):

    streamer_list = get_top_streams(num)["data"]
    return [streamer["user_name"] for streamer in streamer_list]




# temporarily fill database with dummy data

def streams_to_db(num=100):
    
    streams = get_top_streams(num)
    for stream in streams["data"]:
        streamer, created = Streamer.objects.get_or_create(
            username=stream["user_name"],
            platform="Twitch"
        )
        session, created = LiveSession.objects.get_or_create(
            streamer=streamer,
            title=stream["title"],
            is_live=True,
            #start_time=datetime.now()
        )
        Viewership.objects.create(
            live_session = session,
            viewer_count = stream["viewer_count"]
        )
            
        







# if __name__ == "__main__":
#     # print(get_streamer_usernames())
#     print(json.dumps(get_top_streams(1), indent=4))