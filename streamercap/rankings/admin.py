from django.contrib import admin
from .models import Streamer, LiveSession, Viewership
# Register your models here.

admin.site.register(Streamer)
admin.site.register(LiveSession)
admin.site.register(Viewership)

