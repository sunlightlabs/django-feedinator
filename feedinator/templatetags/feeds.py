from django import template
from django.template.loader import render_to_string
from feedinator.models import FeedEntry

register = template.Library()

@register.simple_tag
def headlines(codenames, count, offset=0):
    offset = int(offset)
    index = int(count) + offset
    entries = FeedEntry.objects.filter(feed__codename__in=codenames.split(',')).order_by("-date_published")[offset:index]
    return render_to_string("feedinator/headlines.html", {"entries": entries})