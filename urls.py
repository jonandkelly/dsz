from django.conf.urls.defaults import *

#jss added. enables redirect to index page below
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#only needed for development env
import settings


urlpatterns = patterns('',
    # Example:
    # (r'^myproject/', include('myproject.foo.urls')),

    # only needed for development environment. forces django to serve static media itself.
    # COMMENT THIS OUT WHEN DEPLOYING (need to figure out a more slick way to do this)
    # (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.STATIC_ROOT }),


    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^goals/', include('ds.goals.urls')),
    (r'^account/', include('ds.account.urls')),
    (r'^info/', include('ds.info.urls')),
    (r'^charities/', include('ds.charities.urls')),
    (r'^relationships/', include('relationships.urls')),
    (r'^facebook/', include('django_facebook.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^accounts/', include ('registration.urls')),
    
    # add redirect from '/' URL (added to settings.py) and directly forward it to index.html template

    url(r'^home/', 'ds.goals.views.home', name='home'),
    (r'^charities/', direct_to_template, { 'template': 'charities/index.html' }),
    (r'^networks/', direct_to_template, { 'template': 'networks/index.html' }),
	
    (r'^$', direct_to_template, { 'template': 'index.html' }, 'index'),
)
