from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autofill.views.home', name='home'),
    # url(r'^autofill/', include('autofill.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', 'automail.views.main'),
    url(r'^getmail/', 'automail.views.GetMail'),
    url(r'^deleteDuplicateOrderItem','automail.views.deleteDuplicate'),
    url(r'^auth/', 'automail.views.auth'),
    url(r'^authResult/', 'automail.views.authResult'),
    url(r'^test/', 'automail.views.main'),
)
