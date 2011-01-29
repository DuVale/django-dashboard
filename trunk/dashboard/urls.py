from django.conf.urls.defaults import *

urlpatterns = patterns('djangodashboard.dashboard',
    # Example:
    (r'^view/', 'views.view_gadgets'),
    (r'^gadget/(?P<name>[a-z_0-9]+)/', 'views.gadget'),
    (r'^update-ajax/(?P<name>[a-z_]+)/', 'views.update_ajax'),
    (r'^(?P<name>[a-z_]+)/', 'views.dashboard'),
    
)
