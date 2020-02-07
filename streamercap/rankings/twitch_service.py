import requests
import json
from .models import Streamer, LiveSession, Viewership
from time import sleep

with open('config.json') as config_file:
    config = json.load(config_file)



def get_top_streams(cursor=None):
    URL = f'https://api.twitch.tv/helix/streams?first=100'
    paginated_URL = f'&after={cursor}'
    headers = {'Client-ID': config['TWITCH_ID']}
    if cursor:
        URL = URL + paginated_URL
    r = requests.get(url=URL, headers=headers)
    return r.json()


def get_top_games(num_pages):
    
    
    with open('games.json', 'r') as json_games:
        games_dict = json.loads(json_games.read())

    URL = f'https://api.twitch.tv/helix/games/top?first=100'
    headers = {'Client-ID': config['TWITCH_ID']}
    cursor = "none"
    for i in range(num_pages):
        if cursor != "none":
            paginated_URL = f'&after={cursor}'
            URL = URL + paginated_URL
        r = requests.get(url=URL, headers=headers)

        for game in r.json()["data"]:
            games_dict[game["id"]] = game["name"]

    with open('games.json', 'w') as out_file:
        json.dump(games_dict, out_file, indent=2)


def get_game_by_id(game_id):
    URL = f'https://api.twitch.tv/helix/games?id={game_id}'
    headers = {'Client-ID': config['TWITCH_ID']}
    r = requests.get(url=URL, headers=headers)
    print(r.json())
    sleep(1)
    return r.json()['data'][0]['name']





def streams_to_db(num_pages):
    
    with open('games.json', 'r') as json_games:
        games_dict = json.loads(json_games.read())

    online_streamers = set()
    
    twitch_obj = get_top_streams()
    cursor = twitch_obj["pagination"]["cursor"]
    streams = twitch_obj["data"]
    
    
    for i in range(num_pages):
        twitch_obj = get_top_streams(cursor=cursor)
        cursor = twitch_obj["pagination"]["cursor"]
        streams += twitch_obj["data"]
    
    for stream in streams:
        
        
        streamer, created = Streamer.objects.get_or_create(
            username=stream['user_name'],
            platform='Twitch'
        )
        game_id = stream['game_id']
       
        online_streamers.add(streamer.id)

        try:
            game = games_dict[game_id]
        except KeyError:
            # TODO --- need to handle this exception differently
            #sometimes twitch will return a game an empty game id ''
            if game_id == '': 
                continue

            game_title  = get_game_by_id(game_id)
            game = games_dict[game_id] = game_title
            

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
        
    
    set_streams_offline(online_streamers, 'Twitch')
    
    with open('games.json', 'w') as out_file:
        json.dump(games_dict, out_file, indent=2)




def set_streams_offline(online_streamers, platform):

    offline_streams = LiveSession.objects.filter(is_live=True, streamer__platform=platform).exclude(streamer__in=online_streamers)       
        
    for stream in offline_streams:
        stream.is_live = False
        stream.save()

