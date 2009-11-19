from django import template
from django.template.loader import render_to_string
from feedinator.models import FeedEntry

register = template.Library()

@register.simple_tag
def headlines(codenames, count):
    entries = FeedEntry.objects.filter(feed__codename__in=codenames.split(',')).order_by("-date_published")[:int(count)]
    return render_to_string("feedinator/headlines.html", {"entries": entries})