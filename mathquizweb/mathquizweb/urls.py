from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mathquizweb.views.home', name='home'),
    url(r'^question$', 'mathquizweb.views.question', name='question'),
    url(r'^answer$', 'mathquizweb.views.answer', name='answer'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'mathquizweb.views.register'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
