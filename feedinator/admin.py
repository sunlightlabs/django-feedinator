from django.contrib import admin
from feedinator.models import Feed, FeedEntry, Tag

class TagInline(admin.StackedInline):
    model = Tag

class FeedEntryAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    
admin.site.register(Feed)
admin.site.register(FeedEntry, FeedEntryAdmin)