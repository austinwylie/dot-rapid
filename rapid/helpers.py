from django.db import connection
import jsonpickle
import os
import requests
import shortuuid
import zipfile


def get_uid(hint=None):
    uid = shortuuid.uuid()
    return uid

def transform_wkt(geom, source_srid, target_srid=4326):
    if source_srid == target_srid:
        return geom

    cursor = connection.cursor()
    cursor.execute("SELECT ST_ASTEXT(ST_TRANSFORM('SRID={0};{1}'::geometry, {2}));".format(source_srid, geom, target_srid))
    row = cursor.fetchone()[0]

    return row

def create_wkt(geom_type, coords, parts):
    result = '{0}({1})'
    coords_string = ''

    if not parts or geom_type.lower() == 'LineString'.lower():
        index = 0
        while index < len(coords):
            if index > 0:
                coords_string += ', '
            coords_string += '{0} {1}'.format(str(coords[index][0]), str(coords[index][1]))
            index += 1
    else:
        for i in xrange(len(parts)):
            index = parts[i]

            if index == 0:
                coords_string += '('
                if geom_type.lower() == 'MultiPolygon'.lower():
                    coords_string += '('
            else:
                coords_string += ',('
                if geom_type.lower() == 'MultiPolygon'.lower():
                    coords_string += '('

            while index < len(coords):
                if i + 1 < len(parts) and index >= parts[i + 1]:
                    break
                else:
                    if index > parts[i]:
                        coords_string += ', '
                    coords_string += '{0} {1}'.format(str(coords[index][0]), str(coords[index][1]))
                    index += 1
            coords_string += ')'
            if geom_type.lower() == 'MultiPolygon'.lower():
                coords_string += ')'

    result = result.format(geom_type.upper(), coords_string)
    return result

def dir_zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zf.write(absname, arcname)
    zf.close()
    return zf

def prj_content_to_srid(content):
    try:
        params = {'mode': 'wkt', 'terms': content}
        response = requests.get('http://prj2epsg.org/search.json', params=params)
        srid = response.json()['codes'][0]['code']
        return srid
    except:
        raise Exception('Unable to determine Shapefile\'s projection')

def to_json(params):
    jsonpickle.load_backend('json', 'dumps', 'loads', ValueError)
    jsonpickle.set_preferred_backend('json')
    jsonpickle.set_encoder_options('json', ensure_ascii=False)
    # jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
    # jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
    out = jsonpickle.encode(params, unpicklable=False)
    out = out.replace(': None', ': null')
    return out