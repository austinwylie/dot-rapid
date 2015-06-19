import jsonpickle
from rapid import models


def export_layer(layer, format, start=None, end=None):
    # if layer not found, error
    # if start > end, error
    # etc.

    if format == models.FileType.GEOJSON:
        # return geojson
        pass
    elif format == models.FileType.SHAPEFILE:
        # return shapefile
        pass
    else:
        # error or use default
        pass

def export_geoview(geoview, type, start=None, end=None):
    # and so on
    pass

def to_json(params):
    jsonpickle.load_backend('json', 'dumps', 'loads', ValueError)
    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    # jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    out = jsonpickle.encode(params, unpicklable=False)
    out = out.replace(': None', ': null')
    return out