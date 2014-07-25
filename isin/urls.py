from django.conf.urls import patterns, include, url
from isin import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'in.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^init$', views.init, name='init'),
    url(r'^q$', views.quickinit, name='quick_init'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django_cas.views.login', name='login'),
    url(r'^logout/$', 'django_cas.views.logout', name='logout'),
)
