from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator
from rankings.models import LiveSession, Viewership
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
import json



@csrf_exempt 
def landing(request):

    if request.method == "POST":
        body = json.loads(request.body)
        filters = build_filter_list(body)
        currently_live = LiveSession.objects.filter(**filters).order_by('-viewer_count')
        paginator = Paginator(currently_live, 100)
        try:
            live_dicts = [session.as_dict() for session in paginator.page(body["page"])]
        except EmptyPage: #TODO Handle this on the front end
            live_dicts = {}
        return JsonResponse({"data": live_dicts}) 

    return render(request, 'index.html')


def get_filter_items(request, field, page):

    if field == "platform":
        return JsonResponse({"data": ["Twitch", "Mixer"]})  

    items = LiveSession.objects.all().values(field).annotate(total=Count(field)).order_by('-total')
    
    paginator = Paginator(items, 10)
    top_items = [session[field] for session in paginator.page(page)]
    return JsonResponse({"data": top_items})  


def build_filter_list(filter_data):

    filters = {"is_live":True}
    if filter_data["game"] != []:
        filters["game__in"] = filter_data["game"]
    if filter_data["platform"] != []:
        filters["streamer__platform__in"] = filter_data["platform"]
    if filter_data["language"] != []:
        filters["language__in"] = filter_data["language"]
    
    return filters