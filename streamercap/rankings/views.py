from django.shortcuts import render
from django.db.models import Max, F
from django.core.paginator import Paginator
from rankings.models import LiveSession, Viewership
from .twitch_service import streams_to_db





def landing(request):

    ''' gets most recent Livesessions viewership counts '''
    currently_live = LiveSession.objects.filter(is_live=True).order_by('-viewer_count')


    return render(request, 'index.html', context={"streamers": currently_live})