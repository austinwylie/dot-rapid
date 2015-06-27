from django.core.management import BaseCommand
import time
from datetime import timedelta

from rapid.exporter import Exporter
from rapid.select import *
from rapid.helpers import *
from rapid.models import *
from rapid.importer import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Hello. Welcome to RAPID.'

        token = None
        done = False

        while not done:
            response = raw_input('Please enter your private API key (\'q\' to quit): ')
            response = response.strip()
            print ''

            if response.lower() == 'q':
                print 'Goodbye.'
                return
            elif response.lower() == 'a':
                token = ApiToken.objects.get(key='bbdd303bcf5bde0074e7b451b53941ae0aa18007')
                print 'API token active: {0}'.format(token.descriptor)
                done = True
                done = True
            elif response.lower() == '':
                continue
            else:
                try:
                    token = ApiToken.objects.get(key=response)
                    print 'API token active: {0}'.format(token.descriptor)
                    done = True
                except:
                    print 'This key was not found. You may need to first create an API token.'

        token_params = {'token': token.key}
        token_key = token.key

        print 'Available data and operations:'

        menu_options =[
            '  1 - API Tokens',
            '  2 - GeoViews',
            '  3 - Layers',
        ]

        for each in menu_options:
            print each
        response = raw_input('Select a menu option: ').strip()
        print ''

        base_endpoint = 'http://eddie.cadrc.calpoly.edu:8000/rapid'

        if response == '1':
            r = requests.get(base_endpoint + '/tokens')
            print 'Fetched URL: {0}'.format(r.url)
            print 'API Tokens:'
            for each in r.json():
                print '  {0} - UID: {1} - Key: Private'.format(each['descriptor'], each['uid'])
        elif response == '2':
            r = requests.get(base_endpoint + '/geoview', params=token_params)
            print 'Fetched URL: {0}'.format(r.url)
            print 'Select a GeoView or add a GeoView:'

            count = 0
            for i in xrange(len(r.json())):
                des = r.json()[i]['descriptor']
                print '  ' + str(i) + ' - ' + des
                count = i
            count += 1
            print '  ' + str(count) + ' - Create a GeoView'

            response = raw_input('Select a menu option: ').strip()
            print ''

            try:
                response_num = int(response)
            except:
                print 'Invalid option.'

            if response_num == count:
                print 'Creating a GeoView:'


                raw_input('Save the polygon of interest into geoview.geojson then press any key: ')
                geom = open('data/geoview.geojson', 'r').read().strip()

                des = raw_input('Enter a descriptor: ')
                public = raw_input('Is this a public GeoView (\'y\' or \'n\')? ')

                if public.lower() == 'y':
                    public = True
                else:
                    public = False

                r = requests.post(base_endpoint + '/geoview/', params=token_params, data=json.dumps({"geom": geom, "des": des, "public": public}))
            elif 0 <= response_num < count:
                json_entry = r.json()[response_num]
                geoview_uid = json_entry['uid']

                print 'GeoView: {0}\nUID: {1}'.format(json_entry['descriptor'], geoview_uid)

                menu_options = [
                    '  1 - Add/remove permissions',
                    '  2 - Layers',
                    '  3 - Export',
                    '  4 - Delete'
                ]
                for each in menu_options:
                    print each

                response = raw_input('Select a menu option: ').strip()
                print ''

                if response == '1':
                    print 'Add/remove GeoView Permissions'
                    menu_options = [
                        '  1 - Owner',
                        '  2 - Editor',
                        '  3 - Viewer',
                    ]
                    for each in menu_options:
                        print each

                    role = None
                    while not role:
                        response = raw_input('Select a menu option: ').strip()
                        print ''
                        if response == '1':
                            role = 'owner'
                        elif response == '2':
                            role = 'editor'
                        elif response == '3':
                            role = 'viewer'
                        else:
                            print 'Invalid option.'

                    option = None
                    while not option:
                        response = raw_input('Add or remove {0} (\'a\' or \'r\'): '.format(role)).strip()
                        print ''
                        if response.lower() == 'a':
                            option = 'add'
                        elif response.lower() == 'r':
                            option = 'remove'
                        else:
                            print 'Invalid option.'

                    r = requests.get(base_endpoint + '/tokens')
                    print 'API Tokens:'
                    for each in r.json():
                        print '  {0} - UID: {1}'.format(each['descriptor'], each['uid'])

                    token_uid = None

                    while not token_uid:
                        response = raw_input('Enter the access token\'s UID: ').strip()
                        print ''
                        if len(response) > 0:
                            token_uid = response

                    for each in r.json():
                        if each['uid'] == token_uid:
                            des = each['descriptor']

                    confirm = None
                    while not confirm:
                        response = raw_input(
                            'Confirm (\'y\' or \'n\'): {0} token \'{1}\' as {2}? '.format(option, des, role))
                        print ''
                        if response.lower() == 'y':
                            print 'running'
                            confirm = True
                            r = requests.get(base_endpoint + '/geoview/{0}/{1}/{2}/{3}'.format(geoview_uid, option, role, token_uid), params=token_params)
                            print 'Called endpoint: {0}'.format(r.url)
                            # print r.text
                        elif response.lower() == 'n':
                            print 'Canceled.'
                            confirm = True
                        else:
                            print 'Invalid option.'

                    pass
                elif response == '2':

                    r = requests.get(base_endpoint + '/geoview/{0}'.format(geoview_uid), params=token_params)

                    print 'Accessed endpoint: {0}'.format(r.url)
                    print 'Layers in GeoView:'

                    layers = r.json()['layers']
                    for i in xrange(len(layers)):
                        print '  {0} - {1}'.format(i, layers[i]['descriptor'])

                    if len(layers) == 0:
                        print '  [No layers]'

                    response = raw_input('Select which layer to remove, or enter \'a\' to add a layer or \'b\' to go back: ').strip()

                    option = None
                    while not option:
                        if response.lower() == 'a':
                            all_layers = None
                            r = requests.get(base_endpoint + '/layer/', params=token_params)
                            all_layers = r.json()
                            for i in xrange(len(all_layers)):
                                print '  {0} - {1}'.format(i, all_layers[i]['descriptor'])

                            response = raw_input(
                                'Select a layer to add (or \'b\' to go back): ').strip()

                            if response.isdigit():
                                layer = all_layers[i]
                                r = requests.get(base_endpoint + '/geoview/{0}/add/layer/{1}'.format(geoview_uid, layer['uid']), params=token_params)
                                print 'Accessed endpoint: {0}'.format(r.url)
                                print 'Added layer to GeoView'
                                return
                            elif response.lower() == 'b':
                                pass

                            pass
                        elif response.lower() == 'b':
                            pass
                        elif response.isdigit():
                            choice = int(response)
                            layer = layers[choice]
                            r = requests.get(
                                base_endpoint + '/geoview/{0}/remove/layer/{1}'.format(geoview_uid, layer['uid']),
                                params=token_params)
                            print 'Accessed endpoint: {0}'.format(r.url)
                            print r.text
                            print r.json()['status']
                            print 'Removed layer from GeoView'
                    pass
                elif response == '3':
                    response = raw_input('Only export recent data from last 7 days (\'y\' or \'n\'): ').strip()

                    if response.lower() == 'y':
                        end = datetime.date.today() - timedelta(days=7)
                    else:
                        end = None

                    json_entry = r.json()[response_num]
                    geoview_uid = json_entry['uid']

                    print 'Exporting...'
                    Exporter(token_key).export_geoview(geoview_uid, end=end)
                    print 'Done.'
                    return
                elif response == '4':
                    r = requests.delete('{0}/geoview/{1}'.format(base_endpoint, geoview_uid), params=token_params)
                    print r.json()

        if response == '3':
            r = requests.get(base_endpoint + '/layer/', params=token_params)
            all_layers = r.json()
            print r.url
            print 'Layers'
            count = 0
            for i in xrange(len(all_layers)):
                print '  {0} - {1}'.format(i, all_layers[i]['descriptor'])
                count = i

            count += 1
            print '  {0} - {1}'.format(count, 'Create new layer')

            response = raw_input(
                'Select an option: ').strip()

            if response.isdigit() and int(response) == count:
                des = raw_input('Enter a descriptor: ')
                public = raw_input('Is this a public layer (\'y\' or \'n\')? ')

                if public.lower() == 'y':
                    public = True
                else:
                    public = False

                r = requests.post(base_endpoint + '/layer/', params=token_params,
                                  data=json.dumps({"des": des, "public": public}))
                print r.url
                print '\n\n\n\n'
                print r.text

            elif response.isdigit():
                layer = all_layers[i]
                r = requests.get(base_endpoint + '/layer/{0}'.format(layer['uid']),
                                 params=token_params)
                print 'Accessed endpoint: {0}'.format(r.url)
                print 'Layer: {0}\nUID: {1}'.format(layer['descriptor'], layer['uid'])

                menu_options = [
                    '  1 - Add/remove permissions',
                    '  2 - Export',
                    '  3 - Delete',
                    '  4 - Import'
                ]
                for each in menu_options:
                    print each

                response = raw_input('Select a menu option: ').strip()
                print ''

                if response == '1':
                    print 'Add/remove Layer Permissions'
                    menu_options = [
                        '  1 - Owner',
                        '  2 - Editor',
                        '  3 - Viewer',
                    ]
                    for each in menu_options:
                        print each

                    role = None
                    while not role:
                        response = raw_input('Select a menu option: ').strip()
                        print ''
                        if response == '1':
                            role = 'owner'
                        elif response == '2':
                            role = 'editor'
                        elif response == '3':
                            role = 'viewer'
                        else:
                            print 'Invalid option.'

                    option = None
                    while not option:
                        response = raw_input('Add or remove {0} (\'a\' or \'r\'): '.format(role)).strip()
                        print ''
                        if response.lower() == 'a':
                            option = 'add'
                        elif response.lower() == 'r':
                            option = 'remove'
                        else:
                            print 'Invalid option.'

                    r = requests.get(base_endpoint + '/tokens')
                    print 'API Tokens:'
                    for each in r.json():
                        print '  {0} - UID: {1}'.format(each['descriptor'], each['uid'])

                    token_uid = None

                    while not token_uid:
                        response = raw_input('Enter the access token\'s UID: ').strip()
                        print ''
                        if len(response) > 0:
                            token_uid = response

                    for each in r.json():
                        if each['uid'] == token_uid:
                            des = each['descriptor']

                    confirm = None
                    while not confirm:
                        response = raw_input(
                            'Confirm (\'y\' or \'n\'): {0} token \'{1}\' as {2}? '.format(option, des, role))
                        print ''
                        if response.lower() == 'y':
                            print 'running'
                            confirm = True
                            r = requests.get(
                                base_endpoint + '/layer/{0}/{1}/{2}/{3}'.format(layer['uid'], option, role, token_uid),
                                params=token_params)
                            print 'Called endpoint: {0}'.format(r.url)
                            # print r.text
                        elif response.lower() == 'n':
                            print 'Canceled.'
                            confirm = True
                        else:
                            print 'Invalid option.'
                    pass
                elif response == '2':
                    response = raw_input('Only export recent data from last 7 days (\'y\' or \'n\'): ').strip()

                    if response.lower() == 'y':
                        end = datetime.date.today() - timedelta(days=7)
                    else:
                        end = None

                    print 'Exporting...'
                    Exporter(token_key).export_layer(layer['uid'], end=end)
                elif response == '3':
                    r = requests.delete('{0}/layer/{1}'.format(base_endpoint, layer['uid']), params=token_params)
                    print r.json()
                elif response == '4':
                    for root, dirnames, filenames in os.walk('data/dropbox'):
                        files = []
                        for filename in fnmatch.filter(filenames, '*.zip'):
                            files.append(os.path.join(root, filename))

                        for i in xrange(len(files)):
                            filename = os.path.basename(files[i])
                            filename = os.path.splitext(filename)[0]
                            print '  {0} - {1}'.format(i, filename)

                        response = raw_input('Enter a file to import into the layer: ').strip()
                        if response.isdigit():
                            choice = int(response)

                            importer = Importer(token_key)
                            print 'Importing...'
                            importer.import_shapefile(files[choice], layer['uid'])
                            print 'Done.'
                        else:
                            print 'Invalid choice.'

            elif response.lower() == 'b':
                pass



            else:
                print 'Invalid option.'





