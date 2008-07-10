from django.core.management.base import NoArgsCommand
from optparse import make_option
from feedinator.models import Feed
    
class Command(NoArgsCommand):
    
    help = "Shows all configured feeds"
    
    requires_model_validation = False
    
    def handle_noargs(self, **options):
        feeds = Feed.objects.order_by('title')
        for feed in feeds:
            print u"[%i] %s %s" % (feed.id, feed.title, feed.url)