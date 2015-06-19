import geojson
import shortuuid
import urllib2
from rapid.models import GeoView, DataLayer, Feature, Archive, ApiToken
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point

# FEATURES
def create_feature(geom, layer=None, archive=None, properties=None, Token=None):
    feature = Feature(layer=layer, archive=archive, geom=geom)
    feature.uid = get_uid()
    if properties:
        feature.properties = properties
    feature.save()
    return feature.uid

def delete_geoview(uid, Token=None):
    try:
        GeoView.objects.get(uid=uid).delete()
        return True
    except:
        return False

def delete_layer(uid, Token=None):
    try:
        DataLayer.objects.get(uid=uid).delete()
        return True
    except:
        return False

def delete_feature(uid, Token=None):
    try:
        Feature.objects.get(uid=uid).delete()
        return True
    except:
        return False

def update_feature(uid, geom, layer=None, archive=None, properties=None, Token=None):
    feature = get_feature(uid)
    feature.geom = geom
    feature.layer = layer
    if properties:
        feature.properties = properties
    feature.archive = archive
    feature.save()
    return feature.uid


def get_feature(uid, Token=None):
    feature = Feature.objects.filter(uid=uid)[0]
    return feature


# LAYERS
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
    pass


# GEOVIEWS
def create_geoview(geom, descriptor, properties, token=None):
    view = GeoView(geom=geom, descriptor=descriptor, properties=properties)
    view.uid = get_uid()
    view.save()
    return view.uid


def get_geoviews(Token=None):
    return list(GeoView.objects.all())


def get_geoview(uid, file=False, Token=None):
    if not file:
        geoview = GeoView.objects.filter(uid=uid)[0]
        return geoview
    else:
        return "somefile.geojson"


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


# HELPERS
def import_geojson_file(descriptor, filepath, Token=None):
    content = open(filepath).read()
    import_geojson_content(content, descriptor)


def import_geojson_url(descriptor, endpoint, Token=None):
    f = urllib2.urlopen(endpoint)
    content = f.read()
    import_geojson_content(content, descriptor)


def create_archive(content, layer, mime, Token=None):
    archive = Archive()
    archive.internet_media_type = mime
    archive.content = content
    archive.layer = layer
    archive.save()
    return archive


def import_geojson_content(content, descriptor, Token=None):
    mime = 'application/vnd.geo+json'

    layer = DataLayer()
    layer.descriptor = descriptor
    layer.uid = get_uid()
    layer.save()

    archive = create_archive(content, layer, mime)

    data = geojson.loads(content)

    for feature in data.features:

        out = str(feature.geometry)
        geom = GEOSGeometry(out)

        if isinstance(geom, Point):
            geom = Point(geom[0], geom[1])

        create_feature(geom, layer, archive, feature.properties)

import sys
# from osgeo import osr

# def esriprj2standards(shapeprj_path):
#     prj_file = open(shapeprj_path, 'r')
#     prj_txt = prj_file.read()
#     srs = osr.SpatialReference()
#     srs.ImportFromESRI([prj_txt])
#     print 'Shape prj is: %s' % prj_txt
#     print 'WKT is: %s' % srs.ExportToWkt()
#     print 'Proj4 is: %s' % srs.ExportToProj4()
#     srs.AutoIdentifyEPSG()
#     print 'EPSG is: %s' % srs.GetAuthorityCode(None)

def get_apitoken(key):
    ApiToken.objects.get()

def geojson_to_rapid_features(file):
    pass


def shapefile_to_rapid_features(file):
    pass


def get_uid(hint=None):
    uid = shortuuid.uuid()
    return uid
