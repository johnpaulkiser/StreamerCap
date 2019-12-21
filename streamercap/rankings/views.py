from django.shortcuts import render
from rankings.models import LiveSession



def landing(request):
    currently_live = LiveSession.objects.filter(is_live=True).order_by('-current_viewers')
    print(currently_live)
    context = {
        'streamers': currently_live,
    }
    return render(request, 'index.html', context=context)