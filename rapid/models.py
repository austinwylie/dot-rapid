from django.contrib.gis.db import models
from django_enumfield import enum

import hmac
import json
import shortuuid
import uuid
import datetime
from rapid.helpers import get_uid


class Role(enum.Enum):
    VIEWER = 0
    EDITOR = 1
    OWNER = 2

    labels = {
        VIEWER: 'Viewer',
        EDITOR: 'Editor',
        OWNER: 'Owner'
    }


class FileType(enum.Enum):
    GEOJSON = 0
    SHAPEFILE = 1

    labels = {
        GEOJSON: 'GeoJSON',
        SHAPEFILE: 'Shapefile'
    }

class GeoView(models.Model):
    uid = models.TextField(primary_key=True)
    descriptor = models.TextField()
    geom = models.GeometryField(null=True)
    bbox = models.PolygonField(null=True)
    properties = models.TextField(null=True)
    layers = models.ManyToManyField('DataLayer', null=True)

    # unpublished flags. workaround for including/excluding extra info in output
    include_layers = models.NullBooleanField(null=True)
    include_geom = models.NullBooleanField(null=True)

    objects = models.GeoManager()

    def __str__(self):
        return "GeoView { id: " + str(self.uid) + ", descriptor: " + self.descriptor + " }"

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop('layers', None)
        state['geom'] = {'type': self.geom.geom_type, 'coordinates': self.geom.coords}
        state['layers'] = self.get_features()
        if self.include_layers:
            # state['layers'] = list(self.layers.all().values_list('uid', flat=True))
            state['layers'] = self.get_features()

        if not self.include_geom:
            del state['geom']

        del state['_state']
        return state

    def add_layer(self, layer):
        # error checking here

        self.layers.add(layer)

    def get_features(self):
        results = []
        for layer in self.layers.all():
            features = layer.feature_set.filter(geom__intersects=self.geom)
            results.append({'uid': layer.uid, 'features': list(features.values_list('uid', flat=True))})

        return results


    def remove_layer(self, layer):
        # error checking here

        self.layers.remove(layer)


class DataLayer(models.Model):
    uid = models.TextField(primary_key=True)
    descriptor = models.TextField()
    properties = models.TextField(null=True)
    is_public = models.BooleanField(default=False)

    # unpublished flag. workaround for including/excluding extra info in output
    include_features = models.NullBooleanField(null=True)

    objects = models.GeoManager()

    def __getstate__(self):
        state = self.__dict__.copy()
        # state['features'] = list(self.feature_set.all()[:1])
        if self.include_features:
            # state['features'] = list(self.feature_set.all()[:1])
            state['features'] = list(self.feature_set.all().values_list('uid', flat=True))
            #need to add "include_range" to check for start and stop filter of features
        del state['_state']
        del state['include_features']

        return state


class DataSource(models.Model):
    url = models.TextField(null=True)
    layer = models.ForeignKey('DataLayer', null=True)
    update_interval = models.TimeField(null=True)
    expected_type = models.TextField(null=True)  # internet media type
    properties = models.TextField(null=True)


class Feature(models.Model):
    uid = models.TextField(primary_key=True)
    geom = models.GeometryField(null=True)
    bbox = models.PolygonField(null=True)
    properties = models.TextField(null=True)
    create_timestamp = models.TimeField(auto_now_add=True, null=True, db_index=True)
    layer = models.ForeignKey(DataLayer, null=True)
    hash = models.TextField(null=True, unique=True, db_index=True)
    modified_timestamp = models.TimeField(auto_now=True, null=True)

    objects = models.GeoManager()

    def __str__(self):
        return 'uid {0}, time {1}'.format(self.uid, self.create_timestamp)

    def getGeoJson(self):
        if self.geom:
            return self.geom.geojson
        else:
            return ""

    def __getstate__(self):
        state = self.__dict__.copy()
        state['geometry'] = {'type': self.geom.geom_type, 'coordinates': self.geom.coords}
        state['type'] = 'Feature'
        state['properties'] = json.loads(self.properties)
        del state['_state']
        del state['geom']
        return state


class ApiToken(models.Model):
    uid = models.TextField(primary_key=True)
    key = models.TextField(unique=True, db_index=True)
    descriptor = models.TextField(unique=True)
    issued = models.TimeField(null=True, auto_now_add=True)

    def __init__(self, descriptor):
        super(ApiToken, self).__init__()
        self.uid = get_uid()
        self.key = self.generate_secure_key()
        self.descriptor = descriptor
        self.issued = datetime.datetime.now()

    @staticmethod
    def generate_secure_key():
        try:
            from hashlib import sha1
        except ImportError:
            import sha
            sha1 = sha.sha

        # UUID generated from 16 bytes of randomness from /dev/urandom
        new_uuid = uuid.uuid4()
        friendly_digest = hmac.new(str(new_uuid), digestmod=sha1).hexdigest()
        return friendly_digest

    def __str__(self):
        return self.key + ', ' + self.descriptor


class GeoViewRole(models.Model):
    token = models.ForeignKey(ApiToken)
    role = enum.EnumField(Role)
    geo_view = models.ForeignKey(GeoView)

    objects = models.GeoManager()


class DataLayerRole(models.Model):
    token = models.ForeignKey(ApiToken)
    role = enum.EnumField(Role)
    layer = models.ForeignKey(DataLayer)

    objects = models.GeoManager()