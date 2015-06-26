import fnmatch
import geojson
import os
import shapefile
import shortuuid
import urllib2
from rapid.helpers import *
from rapid.models import GeoView, DataLayer, Feature, ApiToken
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
import json

def get_feature(uid, Token=None):
    feature = Feature.objects.filter(uid=uid)[0]
    return feature

def create_feature(geom, layer=None, archive=None, properties=None, Token=None):
    feature = Feature(layer=layer, geom=geom)
    feature.uid = get_uid()
    if properties:
        feature.properties = properties
    feature.save()
    return feature.uid

def update_feature(uid, geom, layer=None, archive=None, properties=None, Token=None):
    feature = get_feature(uid)
    feature.geom = geom
    feature.layer = layer
    if properties:
        feature.properties = properties
    feature.archive = archive
    feature.save()
    return feature.uid

def delete_feature(uid, Token=None):
    try:
        Feature.objects.get(uid=uid).delete()
        return True
    except:
        return False

def create_layer(descriptor, is_public, properties, Token=None):
    layer = DataLayer(descriptor=descriptor, properties=properties, is_public=is_public)
    layer.uid = get_uid()
    layer.save()
    return layer.uid

def get_layers(Token=None):
    return DataLayer.objects.all()
    pass


def get_layer(uid, start=None, stop=None, Token=None):
    layer = DataLayer.objects.filter(uid=uid)
    if start and stop:
        layer = layer.feature_set.filter(create_timestamp__lte=start, create_timestamp__gte=stop)
    elif start:
        layer = layer.feature_set.filter(create_timestamp__lte=start)
    elif stop:
        layer = layer.feature_set.filter(create_timestamp__gte=stop)
    return layer[0]


def delete_layer(uid, Token=None):
    try:
        DataLayer.objects.get(uid=uid).delete()
        return True
    except:
        return False

def get_geoviews(Token=None):
    return list(GeoView.objects.all())

def get_geoview(uid, file=False, Token=None):
    if not file:
        geoview = GeoView.objects.filter(uid=uid)[0]
        return geoview
    else:
        return "somefile.geojson"

def delete_geoview(uid, Token=None):
    try:
        GeoView.objects.get(uid=uid).delete()
        return True
    except:
        return False

def create_geoview(geom, descriptor, properties, token=None):
    view = GeoView(geom=geom, descriptor=descriptor, properties=properties)
    view.uid = get_uid()
    view.save()
    return view.uid

def add_layer_to_geoview(geoview_uid, layer_uid, Token=None):
    geoview = GeoView.objects.filter(uid=geoview_uid)
    layer = DataLayer.objects.filter(uid=layer_uid)

    if geoview.count() > 0 and layer.count() > 0:
        geoview[0].add_layer(layer[0])
        geoview[0].save()
        return "SUCCESS: ", geoview[0].uid, " + ", layer[0].uid
    return "FAILURE: incorrect uid"


def remove_layer_from_geoview(layer_uid, geoview_uid, Token=None):
    geoview = GeoView.objects.filter(uid=geoview_uid)
    layer = DataLayer.objects.filter(uid=layer_uid)

    # make sure only one geoview and layer
    if geoview.count() > 0 and layer.count() > 0:
        geoview[0].remove_layer(layer[0])
        geoview[0].save()
        return "SUCCESS: ", geoview[0].uid, " + ", layer[0].uid
    return "FAILURE: incorrect uid"

def get_apitoken(uid):
    try:
        return ApiToken.objects.get(uid=uid)
    except:
        return None
