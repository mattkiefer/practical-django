
from django.utils import timezone
from coltrane.models import Category, Entry, Link
from tagging.models import Tag








# tag urls
urlpatterns += patterns('',
    url(r'^tags/$', 'django.views.generic.list_detail.object_list', {'queryset':Tag.objects.all()}),
    url(r'^tags/entries/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list',{'queryset_or_model':Entry,'template_name': 'coltrane/entries_by_tag.html'}),
    url(r'^tags/links/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list',{'queryset_or_model':Link,'template_name': 'coltrane/links_by_tag.html'}),
)

