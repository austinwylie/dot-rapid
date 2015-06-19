# pycharm -> tools -> start ssh session > octo-robot >$ cd stack >$ sudo ./ctlscript.sh restart apache

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rapid.models import DataLayer, GeoView

urlpatterns = patterns('rapid.views',
    # Examples:
    # url(r'^$', 'RAPID.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # GeoViews have DataLayers which have Features (that come from an Archive)
    # Features are stored in a DataLayer



    url(r'^admin/', include(admin.site.urls)),
    url(r'^rapid/layer/$', 'layers'),
    url(r'^rapid/layer/(?P<layer_uid>[\w]+)/', 'getLayer'), #add functionality for query strings of start and stop time
    url(r'^rapid/geoview/$', 'geoviews'),
    url(r'^rapid/geoview/(?P<geo_uid>[\w]+)/$', 'getGeoview'),
    url(r'^rapid/geoview/(?P<geo_uid>[\w]+)/(?P<spatial_operator>[\w]+)/$', 'getGeoviewWithType'),
    url(r'^rapid/feature/$', 'features'),
    url(r'^rapid/import/(?P<layerId>[\w]+)/', 'featuresFromURL'),
    url(r'^rapid/feature/(?P<feature_uid>[\w]+)/$', 'updateFeature'),
    url(r'^rapid/geoview/addlayer/(?P<geo_uid>[\w]+)/(?P<layer_uid>[\w]+)/$', 'addLayerToGeoview'),
    url(r'^rapid/geoview/removelayer/(?P<geo_uid>[\w]+)/(?P<layer_uid>[\w]+)/$', 'removeLayerFromGeoview'),


)
