from django.conf.urls import patterns, include, url
from django.contrib import admin
from rapid.models import DataLayer, GeoView

urlpatterns = patterns('rapid.views',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rapid/layer/$', 'layers'),
    url(r'^rapid/layer/(?P<layer_uid>[\w]+)/', 'getLayer'),
    url(r'^rapid/geoview/$', 'geoviews'),
    url(r'^rapid/geoview/(?P<geo_uid>[\w]+)/$', 'getGeoview'),
    url(r'^rapid/geoview/(?P<geo_uid>[\w]+)/(?P<spatial_operator>[\w]+)/$', 'getGeoviewWithType'),
    url(r'^rapid/feature/$', 'features'),
    url(r'^rapid/import/(?P<layerId>[\w]+)/', 'featuresFromURL'),
    url(r'^rapid/feature/(?P<feature_uid>[\w]+)/$', 'updateFeature'),
    url(r'^rapid/geoview/addlayer/(?P<geo_uid>[\w]+)/(?P<layer_uid>[\w]+)/$', 'addLayerToGeoview'),
    url(r'^rapid/geoview/removelayer/(?P<geo_uid>[\w]+)/(?P<layer_uid>[\w]+)/$', 'removeLayerFromGeoview'),
)
