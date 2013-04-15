import datetime

from django.contrib.auth.models import User
from django.db import models

from markdown import markdown
from tagging.fields import TagField


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
    
class Link(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    description_html = models.TextField(blank=True)
    url = models.URLField(unique=True)
    
    posted_by = models.ForeignKey(User)
    
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date')
    
    tags = TagField()
    
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to Delicious', default=True)
    
    via_name = models.CharField('Via', max_length=250, blank=True, help_text="The name of the person or site where you found the link. Optional")
    via_URL = models.URLField('Via URL', blank=True, help_text="The URL where you found the link. Optional")
    
    class Meta:
        order = ['-pub_date']
        
    def __unicode__(self):
        return self.title
        
    def save(self):
        if self.description:
            self.description_html = markdown(self.description)
        super(Link, self).save()
