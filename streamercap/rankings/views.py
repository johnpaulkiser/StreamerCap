from django.shortcuts import render
from django.db.models import Max, F
from django.core.paginator import Paginator
from rankings.models import LiveSession, Viewership
from .twitch_service import streams_to_db





def landing(request):

    streams_to_db(100)
    ''' gets most recent Livesessions viewership counts '''
    currently_live = LiveSession.objects.filter(is_live=True).order_by('-viewer_count')

    # viewership = [session.viewer_count for session in currently_live]
    # live_ranked = sorted(
    #             zip(currently_live, viewership),
    #             key=lambda views: views[1],
    #             reverse=True
    #         )
    
    # for i in currently_live:
    #     print(f'{i.streamer} -- {i.viewer_count}')

    return render(request, 'index.html', context={"streamers": currently_live})