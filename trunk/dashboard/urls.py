from django.conf.urls.defaults import *

urlpatterns = patterns('djangodashboard.dashboard',
    # Example:
    
    (r'^gadget/(?P<name>[a-z_0-9]+)/', 'views.gadget'),
    (r'^update-ajax/(?P<name>[a-z_]+)/', 'views.update_ajax'),
    (r'^(?P<name>[a-z_]+)/add/(?P<gadget>[a-z_0-9]+)/', 'views.add_gadget'),
    (r'^(?P<name>[a-z_]+)/view-gadgets/', 'views.view_gadgets'),
    (r'^(?P<name>[a-z_]+)/', 'views.dashboard'),
)
