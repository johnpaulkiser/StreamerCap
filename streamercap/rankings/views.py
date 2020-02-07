from django.shortcuts import render
from django.db.models import Max, F
from django.core.paginator import Paginator
from rankings.models import LiveSession, Viewership
from .twitch_service import streams_to_db
from django.http import JsonResponse





def landing(request):

    return render(request, 'index.html')

def default_filters(request):

    ''' gets most recent Livesessions viewership counts '''
    print(request)
    currently_live = LiveSession.objects.filter(is_live=True).order_by('-viewer_count')

    live_dicts = [ session.as_dict() for session in currently_live ]
    return JsonResponse({"data": live_dicts}) 