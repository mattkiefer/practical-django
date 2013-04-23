import datetime

from django.contrib.auth.models import User
from django.db import models

from markdown import markdown
from tagging.fields import TagField

from django.utils.encoding import smart_str

from django.conf import settings

# category model

class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text='Suggested value automatically generated from title. Must be unique.')
    description = models.TextField()
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"
    
    def __unicode__(self):
        return self.title
        
    def get_absolute_url(self):
        return "/categories/%s/" % self.slug

    def live_entry_set(self):
        from coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

# custom manager filters for live entry objects

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)
        
# entry model
        
class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    status = models.IntegerField(choices = STATUS_CHOICES, default = LIVE_STATUS)

    live = LiveEntryManager()
    objects = models.Manager()

    # core fields
    title = models.CharField(max_length=250, help_text='Write a headline here.')
    excerpt = models.TextField(blank=True, help_text='This will appear as an intro to your post.')
    body = models.TextField(help_text='Write your blog entry here.')
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    # fields to store generated html
    excerpt_html = models.TextField(editable=False,blank=True)
    body_html = models.TextField(editable=False,blank=True)
    
    # metadata
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique_for_date='pub_date')
    
    # categorization
    categories = models.ManyToManyField(Category)
    tags = TagField()
    
    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['-pub_date']
        def __unicode__(self):
            return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update)
                    
    def get_absolute_url(self):
        return ('coltrane_entry_detail', (), {'year':self.pub_date.strftime("%Y"),
                                              'month':self.pub_date.strftime("%b").lower(),
                                              'day':self.pub_date.strftime("%d"),
                                              'slug':self.slug })
    
    get_absolute_url = models.permalink(get_absolute_url)
    
# link model
    
class Link(models.Model):
    # Metadata
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to Delicious', default=True, help_text="If checked, this link will be posted to both your weblog and to your del.icio.us account")
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')
    title = models.CharField(max_length=250)
    
    # The actual link bits
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    via_name = models.CharField('Via', max_length=250, blank=True, help_text="The name of the person or site where you found the link. Optional")
    via_URL = models.URLField('Via URL', blank=True, help_text="The URL where you found the link. Optional")
    tags = TagField()
    url = models.URLField(unique=True)    
    
    class Meta:
        ordering = ['-pub_date']
        
    def __unicode__(self):
        return self.title
        
    def save(self):
        if not self.id and self.post_elsewhere:
            import pydelicious
            pydelicious.add(settings.DELICIOUS_USER, settings.DELICIOUS_PASSWORD, smart_str(self.url),smart_str(self.title),smart_str(self.tags))
        if self.description:
            self.description_html = markdown(self.description)
        super(Link, self).save()
        
    def get_absolute_url(self):
        return ('coltrane_link_detail', (), {'year': self.pub_date.strftime('%Y'),
                                            'month': self.pub_date.strftime('%b').lower(),
                                            'day': self.pub_date.strftime('%d'),
                                            'slug': self.slug })

    get_absolute_url = models.permalink(get_absolute_url)
