from django.conf.urls.defaults import *
from coltrane.models import Category

# category urls
urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list',{'queryset':Category.objects.all()}),
    url(r'^(?P<slug>[-\w]+)/$', 'coltrane.views.category_detail'),
)
