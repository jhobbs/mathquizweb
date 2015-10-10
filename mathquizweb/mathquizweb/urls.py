from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'mathquizweb.views.question', name='home'),
    url(r'^stats$', 'mathquizweb.views.stats', name='stats'),
    url(r'^history$', 'mathquizweb.views.history', name='history'),
    url(r'^answer$', 'mathquizweb.views.answer', name='answer'),
    url(r'^question/(?P<question_id>\d+)/$', 'mathquizweb.views.question_detail', name='question'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/register/$', 'mathquizweb.views.register'),
    url(r'^accounts/settings/$', 'mathquizweb.views.settings', name='settings'),

    url(r'^admin/', include(admin.site.urls)),
)
