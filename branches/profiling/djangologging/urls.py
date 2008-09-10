import os

from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^(?P<request_id>[^/]+)/$', 'djangologging.views.profile'),
    (r'^(?P<request_id>[^/]+)/graph/$', 'djangologging.views.profile_graph'),
    (r'^(?P<request_id>[^/]+)/graph/image/$', 'djangologging.views.graph_image'),
    (r'^media/(?P<path>.+)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'media')}),
)