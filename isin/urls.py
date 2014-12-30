from django.conf.urls import patterns, include, url
from isin import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^u$', views.update, name='update'),
    url(r'^q$', views.quick_update, name='quick_update'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django_cas.views.login', name='login'),
    url(r'^logout/$', 'django_cas.views.logout', name='logout'),
)
