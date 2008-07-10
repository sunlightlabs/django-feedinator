from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import feedinator
    
class Command(BaseCommand):
    
    help = "Add a new RSS/Atom feed to be scraped"
    args = '[feed URL] [codename]'
    
    requires_model_validation = False
    
    def handle(self, url=None, codename=None, *args, **options):
        
        if args or not url or not codename:
            raise CommandError('Usage is addfeed %s' % self.args)
        
        feedinator.add_feed(url, codename)