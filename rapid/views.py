from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
import os
from rest_framework.renderers import JSONRenderer
import urllib
import json

from rapid.select import create_layer, get_layers, create_geoview, get_geoviews, add_layer_to_geoview, \
    create_feature, get_feature, update_feature, get_layer, get_geoview, import_geojson_url, \
    remove_layer_from_geoview, delete_feature, delete_layer, delete_geoview
from rapid.helpers import to_json


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def layers(request):
    message = ''
    token = None
    descriptor = None
    properties = None
    is_public = None

    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    if request.method == 'POST':
        jsonDict = json.loads(request.body)

        if jsonDict['des']:
            descriptor = jsonDict['des']
        if jsonDict['public']:
            is_public = jsonDict['public']
        if jsonDict['props']:
            properties = jsonDict['props']

        uid = create_layer(descriptor, is_public, properties, token)
        message = to_json(uid)
        return HttpResponse(message)

    elif request.method == 'GET':
        all_layers = get_layers(token)
        all_layers = list(all_layers)

        for layer in all_layers:
            layer.include_features = False

        message = to_json(all_layers)

        for layer in all_layers:
            layer.include_features = True

        # MAYBE USE api.export.export_layer() FOR THIS?

        pass
    else:
        # dunno
        pass

    return HttpResponse(message)


@csrf_exempt
def geoviews(request):
    message = ''
    geometry = None
    descriptor = None
    properties = None
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    if request.method == 'POST':
        jsonDict = json.loads(request.body)

        if jsonDict['geom']:
            geometry = str(jsonDict['geom']).replace('u\'', '\'')
            print geometry
            geometry = GEOSGeometry(geometry)

        if jsonDict['des']:
            descriptor = jsonDict['des']

        if jsonDict['props']:
            properties = jsonDict['props']

        uid = create_geoview(geometry, descriptor, properties, token)
        message = to_json(uid)
        return HttpResponse(message)

    elif request.method == 'GET':
        all_geoviews = get_geoviews(token)

        for geoview in all_geoviews:
            geoview.include_geom = geoview.include_layers = False

        message = to_json(all_geoviews)

        for geoview in all_geoviews:
            geoview.include_geom = geoview.include_layers = True


        return HttpResponse(message)
    return HttpResponse(message)


@csrf_exempt
def addLayerToGeoview(request, geo_uid, layer_uid):
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    message = add_layer_to_geoview(geo_uid, layer_uid, token)

    #message = "added " + layer_uid + " to " + geo_uid
    return HttpResponse(message)

@csrf_exempt
def removeLayerFromGeoview(request, geo_uid, layer_uid):
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    message = remove_layer_from_geoview(geo_uid, layer_uid, token)

    #message = "added " + layer_uid + " to " + geo_uid
    return HttpResponse(message)

@csrf_exempt
def importGeoJsonLayer(request, url, descriptor):
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    url = urllib.unquote(url).decode('utf8')
    import_geojson_url(descriptor, url, token)

    message = "added.?.?.?"
    return HttpResponse(message)

@csrf_exempt
def features(request):
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    if request.method == 'POST':
        jsonDict = json.loads(request.body)
        if jsonDict['layer']:
            layer = jsonDict['layer']
            layer = get_layer(layer)
        if jsonDict['content']:
            content = jsonDict['content']
            if content['geom']:
                geom = content['geom']
        if jsonDict['props']:
            properties = jsonDict['props']
        # archive = create_archive(content, layer, models.FileType.GEOJSON, token)
        feature = create_feature(geom, layer, archive=None, properties=properties, token=token)
        myjson = to_json(feature)
        return HttpResponse(myjson, content_type='application/json')
    return HttpResponse('must POST')

@csrf_exempt
def featuresFromURL(request, layerId):
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)
    if request.method == 'GET':
        if request.GET.get('url'):
            url = request.GET.get('url')
            url=urllib.unquote(url).decode('utf8')
            print url
            import_geojson_url(layerId, url, token)
    return HttpResponse('must GET')

#required to provide all geojson when updating
@csrf_exempt
def updateFeature(request, feature_uid):
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    if request.method == 'POST':
        jsonDict = json.loads(request.body)
        if jsonDict['layer']:
            layer = jsonDict['layer']
            layer = get_layer(layer, token)
        if jsonDict['content']:
            content = jsonDict['content']
            if content['geom']:
                geom = content['geom']
        if jsonDict['props']:
            properties = jsonDict['props']
        archive = None
        feature = update_feature(feature_uid, geom, layer, archive, properties, token)
        myjson = to_json(feature)
        return HttpResponse(myjson, content_type='application/json')
    if request.method == 'GET':
        feature = get_feature(feature_uid, token)
        myjson = to_json(feature)
        return HttpResponse(myjson, content_type='application/json')
    if request.method == 'DELETE':
        delete_feature(feature_uid, token)
        message = "DELETE layer with uid ", feature_uid, " :: SUCCESS"
        return HttpResponse(message)
    return HttpResponse('ERROR: must POST, GET, or DELETE')


@csrf_exempt
def getLayer(request, layer_uid):
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    if request.method == 'GET':
        start = None
        stop = None
        if request.GET.get('start'):
            start = float(request.GET.get('start'))
        if request.GET.get('stop'):
            stop = float(request.GET.get('stop'))
            #layer = layer.features.filter
        layer = get_layer(layer_uid, start, stop, token)
        layer.include_features = True
        myjson = to_json(layer)
        layer.include_features = False

        return HttpResponse(myjson, content_type='application/json')
    if request.method == 'DELETE':
        delete_layer(layer_uid, token)
        message = "DELETE layer with uid ", layer_uid, " :: SUCCESS"
        return HttpResponse(message)
    return HttpResponse('ERROR: must GET or DELETE')

@csrf_exempt
def getGeoview(request, geo_uid):
    token = None
    # if request.get('token'):
    #     token = request.get('token')
    #     token = get_apitoken(token)

    if request.method == 'GET':
        file = False
        if request.GET.get('file'):
            filepath = get_geoview(geo_uid, file, token)
            return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
        else:
            geoview = get_geoview(geo_uid, token)
            myjson = to_json(geoview)
            return HttpResponse(myjson, content_type='application/json')
    if request.method == 'DELETE':
        delete_geoview(geo_uid, token)
        message = "DELETE geoview with uid ", geo_uid, " :: SUCCESS"
        return HttpResponse(message)
    return HttpResponse('ERROR: must GET or DELETE')
