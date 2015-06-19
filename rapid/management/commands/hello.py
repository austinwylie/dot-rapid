from django.core.management import BaseCommand
from django.db import connection
import random
import sys
from rapid.api.export import to_json
from rapid.database import select
from rapid.models import Feature, GeoView, DataLayer, ApiToken
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.say_hi()
        # self.alexa_things()
        # self.testwoo()
        # self.austin_things()

    def say_hi(self):
        print "Hello world"
        print ''

    def alexa_things(self):
        url = 'http://pipelions.com/rapid/geoview/'
      #  payload = '{ "des": "California Cities", "public": true, "props": {} }'
        payload = '{ "geom": { "coordinates": [ [ [ -121.581354, 36.899152 ], [ -121.581154, 36.919252 ], [ -121.624755, 36.940451 ], [ -121.645791, 36.93233 ], [ -121.654038, 36.950584 ], [ -121.66613, 36.96434 ], [ -121.693303, 36.96823 ], [ -121.695358, 36.98515 ], [ -121.717878, 36.995561 ], [ -121.738627, 36.990085 ], [ -121.718762, 37.007557 ], [ -121.736186, 37.015342 ], [ -121.75562, 37.0491 ], [ -121.809185, 37.069369 ], [ -121.82402, 37.08757 ], [ -121.99109, 37.14427 ], [ -122.015966, 37.165658 ], [ -122.055064, 37.212683 ], [ -122.08981, 37.22327 ], [ -122.152278, 37.286055 ], [ -122.154381, 37.290423 ], [ -122.162209, 37.293656 ], [ -122.165375, 37.296342 ], [ -122.163627, 37.301257 ], [ -122.16823, 37.307807 ], [ -122.17703, 37.312501 ], [ -122.186058, 37.314341 ], [ -122.18734, 37.321535 ], [ -122.184187, 37.325674 ], [ -122.184078, 37.334842 ], [ -122.189767, 37.341497 ], [ -122.197131, 37.352206 ], [ -122.202102, 37.364788 ], [ -122.199288, 37.373563 ], [ -122.193099, 37.382737 ], [ -122.190064, 37.391148 ], [ -122.191779, 37.399802 ], [ -122.193827, 37.411275 ], [ -122.189162, 37.418923 ], [ -122.190423, 37.426335 ], [ -122.185924, 37.433648 ], [ -122.179412, 37.440368 ], [ -122.174787, 37.443861 ], [ -122.167874, 37.44958 ], [ -122.1629, 37.453542 ], [ -122.155715, 37.454907 ], [ -122.150158, 37.457129 ], [ -122.141065, 37.457133 ], [ -122.131827, 37.453782 ], [ -122.126813, 37.453533 ], [ -122.122866, 37.457278 ], [ -122.111974, 37.466438 ], [ -122.081473, 37.477838 ], [ -122.045271, 37.460276 ], [ -121.996671, 37.467239 ], [ -121.975071, 37.460639 ], [ -121.947087, 37.467424 ], [ -121.925548, 37.454389 ], [ -121.855762, 37.484537 ], [ -121.472648, 37.48217 ], [ -121.486775, 37.475652 ], [ -121.462917, 37.451489 ], [ -121.472606, 37.423345 ], [ -121.448163, 37.391677 ], [ -121.42405, 37.393635 ], [ -121.412549, 37.389435 ], [ -121.42365, 37.358837 ], [ -121.40915, 37.330637 ], [ -121.405753, 37.31099 ], [ -121.459068, 37.282319 ], [ -121.45575, 37.24944 ], [ -121.441746, 37.231127 ], [ -121.422711, 37.22236 ], [ -121.399451, 37.150386 ], [ -121.383551, 37.151487 ], [ -121.384552, 37.165507 ], [ -121.354561, 37.183893 ], [ -121.328409, 37.16595 ], [ -121.29773, 37.166429 ], [ -121.281107, 37.183603 ], [ -121.262293, 37.159473 ], [ -121.237712, 37.15758 ], [ -121.226804, 37.134774 ], [ -121.217339, 37.123042 ], [ -121.230439, 37.096942 ], [ -121.245384, 37.089501 ], [ -121.209637, 37.068243 ], [ -121.208198, 37.061289 ], [ -121.223387, 37.057507 ], [ -121.224507, 37.039743 ], [ -121.245989, 37.025575 ], [ -121.233137, 36.999346 ], [ -121.245887, 36.983036 ], [ -121.215406, 36.961248 ], [ -121.418253, 36.96064 ], [ -121.451972, 36.98884 ], [ -121.463561, 36.978294 ], [ -121.488949, 36.983148 ], [ -121.501488, 36.971895 ], [ -121.513813, 36.945155 ], [ -121.558452, 36.910468 ], [ -121.560272, 36.897111 ], [ -121.581354, 36.899152 ] ] ], "type": "Polygon" }, "des": "Santa Clara County, CA", "props": null }'
        #        payload = payload.replace(u"\xe2", u"")
        print payload
        r = requests.post(url, data=payload)

        print r.text
        pass

    def testwoo(self):
        smptid = DataLayer.objects.get(uid='vzLmskC9YPa5ZeGAmwVKrg').id
        mdptid = DataLayer.objects.get(uid='ffYdeyYtUHPwAJzvyrrjJ').id
        lgptid = DataLayer.objects.get(uid='oHXgMsm9CrzerWL48sLnp9').id
        smpoid = DataLayer.objects.get(uid='7LxYP7Atf5YnDgfonLhNJf').id
        mdpoid = DataLayer.objects.get(uid='3xurg4S3h5ZNvXsvgnPd6B').id
        lgpoid = DataLayer.objects.get(uid='jKwBMMojqT8Wzs5kxkuguH').id

        shasta_county = Feature.objects.get(uid='93Ru9G2wEd7NHTQqSktb4V')

        results = list(Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=smptid))
        results = list(Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=mdptid))
        results = list(Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=lgptid))

        results = list(Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=smpoid))
        results = list(Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=mdpoid))
        results = list(Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=lgpoid))

        for query in connection.queries:
            print query
            print ''

        return

    def austin_things(self):

        DataLayer.objects.filter(id__gte=56, id__lte=121).delete()
        DataLayer.objects.filter(id=127).delete()

        # points_layer_sm = select.create_layer("Points sm", True, 'hello properties')
        # polygon_layer_sm = select.create_layer("Polygon sm", True, 'hello properties')
        # points_layer_md = select.create_layer("Points md", True, 'hello properties')
        # polygon_layer_md = select.create_layer("Polygon md", True, 'hello properties')
        # points_layer_lg = select.create_layer("Points lg", True, 'hello properties')
        polygon_layer_lg = select.create_layer("Polygon lg", True, 'hello properties')

        # sm_points = DataLayer.objects.get(uid=points_layer_sm)
        # md_points = DataLayer.objects.get(uid=points_layer_md)
        # lg_points = DataLayer.objects.get(uid=points_layer_lg)
        #
        # sm_pols = DataLayer.objects.get(uid=polygon_layer_sm)
        # md_pols = DataLayer.objects.get(uid=polygon_layer_md)
        lg_pols = DataLayer.objects.get(uid=polygon_layer_lg)

        all_points_layer = DataLayer.objects.get(uid='QJ6oTbnK6iaxp4TbJewYNi')
        all_polygons_layer = DataLayer.objects.get(uid='agRDPtbkZNoGGw3ZSkYmnA')

        polygon_in_shasta = Feature.objects.get(uid='pAaGhrSRaftajxrnRJVWWL')
        point_in_shasta = Feature.objects.get(uid='koRhUHuwdZKoGAh8GZgdtA')

        # select.create_feature(point_in_shasta.geom, sm_points)
        # select.create_feature(point_in_shasta.geom, md_points)
        # select.create_feature(point_in_shasta.geom, lg_points)
        #
        # select.create_feature(polygon_in_shasta.geom, sm_pols)
        # select.create_feature(polygon_in_shasta.geom, md_pols)
        select.create_feature(polygon_in_shasta.geom, lg_pols)

        # count = 0
        # limit = 9
        # to_add = Feature.objects.filter(layer_id=all_points_layer.id)[:limit]
        # while count < limit:
        #     select.create_feature(random.choice(to_add).geom, sm_points)
        #     count += 1
        #
        # print '1'
        #
        # count = 0
        # limit = 999
        # to_add = Feature.objects.filter(layer_id=all_points_layer.id)[:limit]
        # while count < limit:
        #     choice = random.choice(to_add)
        #     select.create_feature(choice.geom, md_points)
        #     count += 1
        #     if count % 10 == 0:
        #         print count
        #
        # print '1'
        #
        # count = 0
        # limit = 99999
        # to_add = Feature.objects.filter(layer_id=all_points_layer.id)[:limit]
        # while count < limit:
        #     select.create_feature(random.choice(to_add).geom, lg_points)
        #     count += 1
        #     if count % 100 == 0:
        #         print count
        #
        # print '1'
        #
        # count = 0
        # limit = 9
        # to_add = Feature.objects.filter(layer_id=all_polygons_layer.id)[:limit]
        # while count < limit:
        #     select.create_feature(random.choice(to_add).geom, sm_pols)
        #     count += 1
        #
        # print '1'
        #
        # count = 0
        # limit = 999
        # to_add = Feature.objects.filter(layer_id=all_polygons_layer.id)[:limit]
        # while count < limit:
        #     select.create_feature(random.choice(to_add).geom, md_pols)
        #     count += 1

        print '1'

        count = 0
        limit = 99999
        to_add = Feature.objects.filter(layer_id=all_polygons_layer.id)[:limit]
        while count < limit:
            select.create_feature(random.choice(to_add).geom, lg_pols)
            count += 1
            if count % 100 == 0:
                print count

        print '1'
        print 'done'

        shasta_county = Feature.objects.get(uid='93Ru9G2wEd7NHTQqSktb4V')

        return

        smptid = DataLayer.objects.get(uid=points_layer_sm)
        mdptid = DataLayer.objects.get(uid=points_layer_md)
        lgptid = DataLayer.objects.get(uid=points_layer_lg)
        smpoid = DataLayer.objects.get(uid=polygon_layer_sm)
        mdpoid = DataLayer.objects.get(uid=polygon_layer_md)
        lgpoid = DataLayer.objects.get(uid=polygon_layer_lg)

        results = Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=smptid)
        results = Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=mdptid)
        results = Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=lgptid)

        results = Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=smpoid)
        results = Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=mdpoid)
        results = Feature.objects.filter(geom__intersects=shasta_county.geom, layer_id=lgpoid)

        for query in connection.queries:
            print query
            print '\n'

        return

        import sys

        print sys.path

        # try:
        #     from osgeo import ogr, osr, gdal
        # except:
        #     sys.exit('ERROR: cannot find GDAL/OGR modules')

        # esriprj2standards('data/WA/WA_Cowlitz_StreetCenterlines/StreetCenterlines.prj')



        # extract zip file
        # for file in zip:
        # find dbf, prj, and shp
        # use pyshp
        # make new features



        return


        token = ApiToken("Austin")
        print token
        token.save()
        print token


        return
        # sys.setrecursionlimit(50000)
        for layer in DataLayer.objects.all().order_by('?'):
            print layer.descriptor
            for feature in layer.feature_set.all():
                print feature.getGeoJson()
            print '\n\n\n\n\n'

        return
        print "SLO county's 1.0+ earthquakes in previous 7 days:"
        slo = GeoView.objects.get(descriptor='San Luis Obispo')
        results = Feature.objects.filter(geom__within=slo.geom)
        for r in results:
            print r.geom.geojson

