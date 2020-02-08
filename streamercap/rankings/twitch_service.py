import requests
import json
from .models import Streamer, LiveSession, Viewership
from time import sleep, time

with open('config.json') as config_file:
    config = json.load(config_file)



def make_streams_request(cursor=None):
    URL = f'https://api.twitch.tv/helix/streams?first=100'
    paginated_URL = f'&after={cursor}'
    headers = {'Client-ID': config['TWITCH_ID']}
    if cursor:
        URL = URL + paginated_URL
    r = requests.get(url=URL, headers=headers)
    return r.json()


def get_top_games(num_pages):
    ''' Queries the twitch api to get the top (num_pages*100) games '''
    # open games file
    with open('games.json', 'r') as json_games:
        games_dict = json.loads(json_games.read())

    URL = f'https://api.twitch.tv/helix/games/top?first=100'
    headers = {'Client-ID': config['TWITCH_ID']}
    cursor = "none"

    for i in range(num_pages):

        # set url to paginated_url
        if cursor != "none":
            paginated_URL = f'&after={cursor}'
            URL = URL + paginated_URL
            
        response = requests.get(url=URL, headers=headers).json()
        
        # update the pagination cursor
        cursor = response["pagination"]["cursor"]
        
        # store games as keys in dictionary
        for game in response["data"]:
            games_dict[game["id"]] = game["name"]

    #save games dictionary to file
    with open('games.json', 'w') as out_file:
        json.dump(games_dict, out_file, indent=2)



def get_game_by_id(game_id):
    URL = f'https://api.twitch.tv/helix/games?id={game_id}'
    headers = {'Client-ID': config['TWITCH_ID']}
    try:
        r = requests.get(url=URL, headers=headers)
    except:
        sleep(0.5)
        r = requests.get(url=URL, headers=headers)
    print(r.json())
    return r.json()['data'][0]['name']





def get_top_streams():
    ''' continues to query twitch api for 
        top streams until reaching a stream 
        with less than 100 viewers.          
    '''
    start = time()
    with open('games.json', 'r') as json_games:
        games_dict = json.loads(json_games.read())

    online_streams = set()
    cursor = None
    
    while True: # loops untill reaching 100 viewers

        twitch_obj = make_streams_request(cursor=cursor)
        cursor = twitch_obj["pagination"]["cursor"]
        streams = twitch_obj["data"]
        print("Querying twitch api...")
        for stream in streams:
            
            if stream['viewer_count'] < 100:
                set_streams_offline(online_streams, 'Twitch')
                with open('games.json', 'w') as out_file:
                    json.dump(games_dict, out_file, indent=2)
                    end = time()
                print(f"Finished Querying {len(online_streams)} streams from twitch in {end - start} seconds")
                return
            id = stream_to_db(stream, games_dict)
            if id == -1: # catch twitch not returning proper game id
                continue
            online_streams.add(id)

            
            
        
def stream_to_db(stream, games_dict):
    streamer, created = Streamer.objects.get_or_create(
        username=stream['user_name'],
        platform='Twitch'
    )
    game_id = stream['game_id']

    try:
        game = games_dict[game_id]
    except KeyError:
        # TODO --- need to handle this exception differently
        #sometimes twitch will return a game an empty game id ''
        if game_id == '': 
            return -1

        game_title  = get_game_by_id(game_id)
        if game_title == "Just Chatting":
           game_title = "IRL"

        game = games_dict[game_id] = game_title
        

    session, created = LiveSession.objects.get_or_create(
        streamer=streamer,
        is_live=True,
    )
    session.language = stream['language']
    session.title = stream['title']
    session.game = game
    
    Viewership.objects.create(
        live_session = session,
        viewer_count = stream['viewer_count']
    )
    session.set_viewer_count()
    session.save()

    return streamer.id



def set_streams_offline(online_streamers, platform):

    offline_streams = LiveSession.objects.filter(is_live=True, streamer__platform=platform).exclude(streamer__in=online_streamers)       
    for stream in offline_streams:
        stream.is_live = False
        stream.save()

