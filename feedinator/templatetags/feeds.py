from django import template
from django.template.loader import render_to_string
from feedinator.models import FeedEntry

register = template.Library()

@register.simple_tag
def headlines(codename, count):
    entries = FeedEntry.objects.filter(feed__codename=codename).order_by("-date_published")[:int(count)]
    return render_to_string("feedinator/headlines.html", {"entries": entries})