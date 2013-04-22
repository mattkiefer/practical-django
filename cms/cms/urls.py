from django.conf.urls.defaults import *
from django.contrib import admin
from django.utils import timezone

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/user/javascript/tinymce/jscripts/tiny_mce/'}),
    url(r'^search/$', 'search.views.search'),
    url(r'^weblog/',include('coltrane.urls.entries')),
    url(r'^weblog/links/',include('coltrane.urls.links')),
    url(r'^weblog/categories/',include('coltrane.urls.categories')),
    url(r'^weblog/tags/',include('coltrane.urls.tags')),
    url(r'', include('django.contrib.flatpages.urls')),
)
