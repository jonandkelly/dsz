
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^downsize/', include('downsize.foo.urls')),

    (r'^$', 'ds.charities.views.index'),
    (r'^causes/category/(?P<category_id>\d+)/(?P<category_slug>[-\w]+)/$', 'ds.charities.views.listbycategory'),
    (r'^newcharity/$', 'ds.charities.views.newcharity'),
    (r'^addqueued/(?P<charity_id>\d+)/$', 'ds.charities.views.addqueued'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
