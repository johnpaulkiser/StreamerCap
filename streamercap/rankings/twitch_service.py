import requests
import json
from .models import Streamer, LiveSession, Viewership


with open('/etc/config.json') as config_file:
    config = json.load(config_file)



def get_top_streams(num=1000):
    URL = f'https://api.twitch.tv/helix/streams?first={num}'
    headers = {'Client-ID': config['TWITCH_ID']}
    r = requests.get(url=URL, headers=headers)
    return r.json()



def get_game_by_id(game_id):
    URL = f'https://api.twitch.tv/helix/games?id={game_id}'
    headers = {'Client-ID': config['TWITCH_ID']}
    r = requests.get(url=URL, headers=headers)
    return r.json()['data'][0]['name']



def streams_to_db(num=100):
    
    with open('games.json', 'r') as json_games:
        games_dict = json.loads(json_games.read())
    online_streamers = set()

    streams = get_top_streams(num)
    for stream in streams['data']:
        
        
        streamer, created = Streamer.objects.get_or_create(
            username=stream['user_name'],
            platform='Twitch'
        )
        game_id = stream['game_id']
        online_streamers.add(streamer.id)
        try:
            game = games_dict[game_id]
        except KeyError:
            game = games_dict[game_id] = get_game_by_id(game_id)
            

        session, created = LiveSession.objects.get_or_create(
            streamer=streamer,
            is_live=True,
        )
        session.title = stream['title']
        session.game = game
        
        Viewership.objects.create(
            live_session = session,
            viewer_count = stream['viewer_count']
        )
        session.set_viewer_count()
        session.save()
        
    
    set_streams_offline(online_streamers)
    
    with open('games.json', 'w') as out_file:
        json.dump(games_dict, out_file, indent=2)


def set_streams_offline(online_streamers):

    offline_streams = LiveSession.objects.filter(is_live=True).exclude(streamer__in=online_streamers)       
        
    for stream in offline_streams:
        stream.is_live = False
        stream.save()

