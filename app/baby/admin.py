from django.contrib import admin

# Register your models here.

from .models import BabyInfo,BabySitterInfo,Daiper,Feed

#add table to build-in backend admin panel

admin.site.register(BabyInfo)
admin.site.register(BabySitterInfo)
admin.site.register(Daiper)
admin.site.register(Feed)
