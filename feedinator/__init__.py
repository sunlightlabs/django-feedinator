from django.conf import settings
from datetime import datetime
from feedinator.models import Feed, FeedEntry, Tag
from sunlightcore.tz import Eastern, utc
import feedparser
import time

def tuple_to_datetime(t, tz=None):
    """
    Convert a time tuple into a datetime object in the given timezone.
    """
    dt = datetime(
        year=t[0],
        month=t[1],
        day=t[2],
        hour=t[3],
        minute=t[4],
        second=t[5],
        tzinfo=tz
    )
    if tz:
        dt = dt + tz.utcoffset(dt)
    return dt.replace(tzinfo=None)
    
def add_feed(url, codename):
    
    """
    Add a feed to the scraped feeds list.
    """
    
    feed_exists = Feed.objects.filter(url=url).count()
    
    if not feed_exists:
        
        f = feedparser.parse(url)
        
        feed = Feed(
            url = url,
            codename = codename,
            title = f.feed.get("title", codename),
            link = f.feed.get("link", url),
            description = f.feed.get("subtitle", ""),
            ttl = f.feed.get("ttl", 60),
            date_added = datetime.now()
        )
        
        feed.save()

def update_feeds(all_feeds=False):
    
    """
    Update entries from feeds if they are stale.
    Use the --all option to update all feeds regardless of freshness.
    """
    
    feed_ids = Feed.objects.values_list('id', flat=True).order_by("last_fetched")
    
    if not all_feeds:
        feed_ids = feed_ids.filter(next_fetch__lte=datetime.now())
    
    for feed_id in feed_ids:
        update_feed(feed_id)
        
def update_feed(feed_id):
    
    tz = Eastern
    
    """
    Update an individual feed regardless of freshness.
    """
    
    feed = Feed.objects.get(pk=feed_id)
    #FeedEntry.objects.filter(feed=feed).delete()
    
    if settings.DEBUG:
        print "--- updating %s" % feed.title
    
    f = feedparser.parse(feed.url)
    
    for entry in f.entries:
        
        if not "id" in entry:
            if settings.DEBUG:
                print "!!!", entry.title, "has no id"
            continue
        
        entry_exists = feed.entries.filter(uid=entry.id).count()
        
        if not entry_exists:
            
            fe = FeedEntry(
                feed = feed,
                uid = entry.id,
                title = entry.title,
                link = entry.link,
                date_updated = tuple_to_datetime(entry.updated_parsed, tz),
                last_fetched = datetime.now()
            )
            
            fe.summary = entry.get("summary", "")
            if "content" in entry:
                for content in entry.content:
                    fe.content = content.get("value", "")
            else:
                fe.content = entry.get("summary", "")
            
            if "published_parsed" in entry:
                fe.date_published = tuple_to_datetime(entry.published_parsed, tz)
            else:
                fe.date_published = tuple_to_datetime(entry.updated_parsed, tz)
                
            if "author_detail" in entry:
                fe.author_name = entry.author_detail.get("name", "")
                fe.author_email = entry.author_detail.get("email", None)
                fe.author_uri = entry.author_detail.get("href", None)
            elif "author" in entry:
                fe.author_name = entry.author
            
            fe.save()
            
            if "tags" in entry:
                for name in entry.tags:
                    Tag(name=name.term, feed_entry=fe).save()
            
            if settings.DEBUG:
                print fe
            
        else:
            
            fe = FeedEntry.objects.get(uid=entry.id, feed=feed)
            
            if fe.date_updated < tuple_to_datetime(entry.updated_parsed, tz):
                
                fe.title = entry.title
                fe.date_updated = tuple_to_datetime(entry.updated_parsed, tz)
                fe.last_fetched = datetime.now()
                
                fe.summary = entry.get("summary", "")
                if entry.has_key("content"):
                    for content in entry.content:
                        fe.content = content.get("value", "")
                else:
                    fe.content = entry.get("summary", "")
                
                fe.save()
                
                if "tags" in entry:
                    fe.tags.all().delete()
                    for name in entry.tags:
                        Tag(name=name.term, feed_entry=fe).save()
                
                if settings.DEBUG:
                    print "UPDATED %s" % fe
                
    feed.last_fetched = datetime.now()
    feed.save()
            