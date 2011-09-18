
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^downsize/', include('downsize.foo.urls')),

    url (r'^$', 'ds.goals.views.index', name='goal'),
    (r'^summary/(?P<goal_id>\d+)/$', 'ds.goals.views.summary'),
    (r'^dashboard/$', 'ds.goals.views.dashboard'),
    (r'^newgoal/$', 'ds.goals.views.newgoal'),
    (r'^cleargoal/(?P<goal_id>\d+)/$', 'ds.goals.views.cleargoal'),
    (r'^saving/(?P<savingcategory_id>\d+)/(?P<saving_category>[-\w]+)/$', 'ds.goals.views.savingcategory'),
    (r'^newsaving/$', 'ds.goals.views.newsaving'),
    (r'^addsaving/(?P<saving_id>\d+)/(?P<saving_slug>[-\w]+)/$', 'ds.goals.views.addsaving'),
    (r'^movetotop/(?P<goal_id>\d+)/$', 'ds.goals.views.movetotop'),
    (r'^moveup/(?P<goal_id>\d+)/$', 'ds.goals.views.moveup'),
    (r'^movedown/(?P<goal_id>\d+)/$', 'ds.goals.views.movedown'),
    (r'^deletegoal/(?P<goal_id>\d+)/$', 'ds.goals.views.deletegoal'),
    (r'^downsize/$', 'ds.goals.views.downsize'),
    (r'^downsize/edit/(?P<downsize_id>\d+)/$', 'ds.goals.views.editdownsize'),
    (r'^downsize/delete/(?P<downsize_id>\d+)/$', 'ds.goals.views.deletedownsize'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
