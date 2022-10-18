from webbrowser import get
import sqlalchemy
import sys
import json
import ckan.config.middleware
from ckan import model
from ckan.common import config
from ckan.tests.helpers import CKANTestApp, CKANTestClient

from ckan.tests import factories

# Minimum config required for basic app
config["testing"] = True
config['__file__'] = '/srv/app/test.ini'
config['SECRET_KEY'] = 'asdf'
config['here'] = config['__file__']
config['who.config_file'] = '/srv/app/who.ini'
config['beaker.session.secret'] = 'asdf'

# Create app
app = ckan.config.middleware.make_app(config)
test_app = CKANTestApp(app)


def get_organization_id():
    res = test_app.post('/api/action/organization_show', data={'id': 'myorg'})
    return json.loads(res.body)['result']['id']


# org_id = get_organization_id()

# Without the app context, db operations won't work
with test_app.flask_app.app_context():
    # try:
    #     user = factories.Sysadmin(name='asdfs')
    #     user_name = user['name'].encode('ascii')
    #     print('User created')
    # except sqlalchemy.exc.IntegrityError:
    #     print('User exists')

    # # Create organization
    # try:
    #     organization = factories.Organization(name='myorg')
    # except sqlalchemy.exc.InvalidRequestError:
    #     print('Org exists')

    # Create datasets
    dataset = {
        'public_access_level': 'public',
        'unique_id': '',
        'contact_name': 'Jhon',
        'program_code': '018:001',
        'bureau_code': '019:20',
        'contact_email': 'jhon@mail.com',
        'publisher': 'Publicher 01',
        'modified': '2019-01-27 11:41:21',
        'tag_string': 'tag01,tag02',
        'owner_org': '1234',
    }

    d1 = dataset.copy()
    d1.update({'title': 'test 01 dataset', 'unique_id': 't1'})
    dataset1 = factories.Dataset(**d1)
    print('Dataset 1 created')
    d2 = dataset.copy()
    d2.update({'title': 'test 02 dataset', 'unique_id': 't2'})
    dataset2 = factories.Dataset(**d2)
    print('Dataset 2 created')
    d3 = dataset.copy()
    d3.update({'title': 'test 03 dataset', 'unique_id': 't3'})
    dataset3 = factories.Dataset(**d3)
    print('Dataset 3 created')
    d4 = dataset.copy()
    d4.update({'title': 'test 04 dataset', 'unique_id': 't4'})
    dataset4 = factories.Dataset(**d4)
    print('Dataset 4 created')
    d5 = dataset.copy()
    d5.update({'title': 'test 05 dataset', 'unique_id': 't5'})
    dataset5 = factories.Dataset(**d5)
    print('Dataset 5 created')
