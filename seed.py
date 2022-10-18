import ckan.config.middleware
from ckan.common import config
from ckan.tests.helpers import CKANTestApp, CKANTestClient

from ckan.tests import factories

config["testing"] = True
config['__file__'] = '/srv/app/test.ini'
config['SECRET_KEY'] = 'asdf'
config['here'] = config['__file__']
config['who.config_file'] = '/srv/app/who.ini'
config['beaker.session.secret'] = 'asdf'

app = ckan.config.middleware.make_app(config)

print(app._wsgi_app)
print(type(app._wsgi_app))
print(dir(app._wsgi_app))
with app._wsgi_app.app_context():
    user = factories.Sysadmin(name='asdfs')
    user_name = user['name'].encode('ascii')
    organization = factories.Organization(name='myorg',
                                          users=[{'name': user_name, 'capacity': 'Admin'}])
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
            'owner_org': organization['id'],
        }
    d1 = dataset.copy()
    d1.update({'title': 'test 01 dataset', 'unique_id': 't1'})
    dataset1 = factories.Dataset(**d1)
    d2 = dataset.copy()
    d2.update({'title': 'test 02 dataset', 'unique_id': 't2'})
    dataset2 = factories.Dataset(**d2)
    d3 = dataset.copy()
    d3.update({'title': 'test 03 dataset', 'unique_id': 't3'})
    dataset3 = factories.Dataset(**d3)
    d4 = dataset.copy()
    d4.update({'title': 'test 04 dataset', 'unique_id': 't4'})
    dataset4 = factories.Dataset(**d4)
    d5 = dataset.copy()
    d5.update({'title': 'test 05 dataset', 'unique_id': 't5'})
    dataset5 = factories.Dataset(**d5)
