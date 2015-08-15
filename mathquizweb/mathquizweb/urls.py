from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'mathquizweb.views.question', name='home'),
    url(r'^stats$', 'mathquizweb.views.home', name='stats'),
    url(r'^answer$', 'mathquizweb.views.answer', name='answer'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'mathquizweb.views.register'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
