from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wpath.views.home', name='home'),
    # url(r'^wpath/', include('wpath.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'template'}),                           
    url(r'^$', "views.index"),
    url(r'^test/(?P<start>\w+)/(?P<end>\w+)$', "views.test"),

)
