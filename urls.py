from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    ('^code/$', 'coding.views.code'),
    ('^code/([A-Za-z]+)/$', 'coding.views.code'),
    ('^code/([A-Za-z]+)/([A-Za-z0-9\-]+)$', 'coding.views.code'),
    ('^create/$', 'coding.views.create'),
    ('^$', 'views.root'),
)
