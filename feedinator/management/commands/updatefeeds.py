from django.core.management.base import NoArgsCommand
from optparse import make_option
import feedinator
    
class Command(NoArgsCommand):
    
    help = "Updates outdated RSS and Atom feeds"
    
    requires_model_validation = False
    
    NoArgsCommand.option_list += (
        make_option("--all", action='store_true', dest='all', default=False,
            help="update all feeds regardless of last fetched"),
    )
    
    def handle_noargs(self, **options):
        feedinator.update_feeds(options.get("all"))