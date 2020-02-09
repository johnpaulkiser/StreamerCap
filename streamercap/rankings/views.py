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

        #build custom query for streaming length filters
        
        if body["length"] != []:
            currently_live = build_delta_time_qs(body["length"], currently_live)
    
        paginator = Paginator(currently_live, 100)
        try:
            live_dicts = [session.as_dict() for session in paginator.page(body["page"])]
        except EmptyPage: #TODO Handle this on the front end
            live_dicts = {}
        return JsonResponse({"data": live_dicts}) 

    return render(request, 'index.html')


def get_filter_items(request, field, page):

    if field == "length":
        return JsonResponse({"data":["-30 mins", 
                                    "-1:30 hrs", 
                                    "1:30 hrs - 3 hrs", 
                                    "3 hrs - 5 hrs",
                                    "5 hrs - 7 hrs",
                                    "+7 hrs"
                                    ]})

    if field == "platform":
        return JsonResponse({"data": ["Twitch", "Mixer"]})  

    items = LiveSession.objects.filter(is_live=True).values(field).annotate(total=Count(field)).order_by('-total')

    if field == "game":
        return JsonResponse({"data": [session["game"] for session in items]})
    
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

#TODO :: Really needs TESTS
def build_delta_time_qs(times, query):
    

    ''' builds custom query for streaming length filters '''
    result = LiveSession.objects.none()

    if "-30 mins" in times:
        # 30 = num mins, 60 = secs/min => 1800
        
        q1 = query.filter(delta_time__lt=30*60) 
        result = q1 
        
    if "-1:30 hrs" in times:
        q2 = query.filter(delta_time__lt=60*60*1.5) 
        result = result | q2

    if "1:30 hrs - 3 hrs" in times:
        q3 = query.filter(delta_time__gt=60*60*1.5).filter(delta_time__lt=60*60*3)
        result = result | q3

    if "3 hrs - 5 hrs" in times:
        q4 = query.filter(delta_time__gt=60*60*3).filter(delta_time__lt=60*60*5)
        result = result | q4

    if "5 hrs - 7 hrs" in times:
        q5 = query.filter(delta_time__gt=60*60*5).filter(delta_time__lt=60*60*7)
        result = result | q5

    if "+7 hrs" in times:
        q6 = query.filter(delta_time__gt=60*60*7)
        result = result | q6

    return result
    