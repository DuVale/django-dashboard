from django.conf.urls.defaults import *

uuid_re = r'\b[A-F0-9]{8}(?:-[A-F0-9]{4}){3}-[A-Z0-9]{12}\b'

urlpatterns = patterns('djangodashboard.dashboard',
    
    url(r'^gadget/(?P<uuid>'+uuid_re+')/$', 'views.gadget', name="view_gadget"),
    url(r'^update-ajax/(?P<name>[a-z_]+)/$', 'views.update_ajax'),
    url(r'^(?P<name>[a-z_]+)/add/(?P<gadget>[a-z_0-9]+)/$', 'views.add_gadget', name="add_gadget"),
    url(r'^(?P<name>[a-z_]+)/view-gadgets/$', 'views.view_gadgets',name="view_gadgets"),
    url(r'^(?P<name>[a-z_]+)/$', 'views.dashboard'),
)
