from django.conf.urls.defaults import *

urlpatterns = patterns('mysite.dashboard',
    # Example:
    (r'^view/', 'views.view_widgets'),
    (r'^widget/(?P<name>[a-z_0-9]+)/', 'views.widget'),
    (r'^update-ajax/(?P<name>[a-z_]+)/', 'views.update_ajax'),
    (r'^(?P<name>[a-z_]+)/', 'views.dashboard'),
    
)
