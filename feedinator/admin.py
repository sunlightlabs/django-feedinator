from django.contrib import admin
from feedinator.models import Feed, FeedEntry
    
admin.site.register(Feed)
admin.site.register(FeedEntry)