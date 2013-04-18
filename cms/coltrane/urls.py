from django.conf.urls.defaults import *
from django.utils import timezone
from coltrane.models import Entry, Link

# entry date-based query kwargs
entry_info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}    

# link date-based query kwargs
link_info_dict = {
    'queryset': Link.objects.all(),
    'date_field': 'pub_date',
}

# entry and link urls - generic
urlpatterns = patterns('django.views.generic.date_based',
    url(r'^$', 'archive_index',entry_info_dict,'coltrane_entry_archive_index'),
    url(r'^(?P<year>\d{4})/$','archive_year',entry_info_dict,'coltrane_entry_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$','archive_month', entry_info_dict,'coltrane_entry_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$','archive_day', entry_info_dict,'coltrane_entry_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$','object_detail', entry_info_dict,'coltrane_entry_detail'),
    url(r'^links/$', 'archive_index', link_info_dict, 'coltrane_link_archive_index'),
    url(r'^links/(?P<year>\d{4})/$', 'archive_year', link_info_dict, 'coltrane_link_archive_year'),
    url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', link_info_dict, 'coltrane_link_archive_month'),
    url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', link_info_dict, '   coltrane_link_archive_day'),
    url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$','object_detail', link_info_dict, 'coltrane_link_detail'), 
)

# category urls
urlpatterns += patterns('coltrane.views',
    url(r'^categories/$', 'category_list'),
    url(r'^categories/(?P<slug>[-\w]+)/$', 'category_detail'),
)
