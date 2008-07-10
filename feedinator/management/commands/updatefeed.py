from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import feedinator
    
class Command(BaseCommand):
    
    help = "Update a specific RSS/Atom feed"
    args = '[feed id]'
    
    requires_model_validation = False
    
    def handle(self, feed_id=None, *args, **options):
        
        if args or not feed_id:
            raise CommandError('Usage is updatefeed %s' % self.args)
        
        feedinator.update_feed(feed_id)