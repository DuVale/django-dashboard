from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()
import settings

urlpatterns = patterns('',
    (r'^dashboard/', include('django-dashboard.dashboard.urls')),
    (r'^accounts/login/$', 'django-dashboard.login.login_user'),
    (r'^accounts/logout/$', 'django-dashboard.login.logout_user'),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
