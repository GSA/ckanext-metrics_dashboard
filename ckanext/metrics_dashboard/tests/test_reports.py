import pytest
from unittest import TestCase
import ckan.tests.factories as core_factories
from ckan.plugins import toolkit
import ckan.model as model
from ckan.tests.helpers import reset_db
from ckan.lib.search import rebuild
import ckanext.metrics_dashboard.reports as report


@pytest.mark.ckan_config('ckan.plugins', 'metrics_dashboard report harvest datajson_harvest')
@pytest.mark.use_fixtures('with_plugins', 'clean_db')
class TestMetricsDashboard():
    @classmethod
    def setup_method(self):
        reset_db()
        rebuild()

    def test_get_harvest_results(self, app):
        user = core_factories.Sysadmin(name='asdfs')
        organization = core_factories.Organization(name='myorg')
        source_dict = {
            'title': 'Test Source',
            'name': 'test-source',
            'url': 'raw.githubusercontent.com/GSA/catalog.data.gov/main/tests/harvest-sources/data.json',
            'frequency': "MANUAL",
            'source_type': 'datajson',
            'owner_org': organization['id']
        }

        context = {
            "model": model,
            "session": model.Session,
            "user": user['id']
        }
        try:
            harvest_source = toolkit.get_action('harvest_source_create')(
                context,
                source_dict)
            print('harvest source created')
        except toolkit.ValidationError:
            harvest_source = toolkit.get_action('harvest_source_show')(
                context,
                {'id': harvest_source['name']}
            )
            print('harvest source exists')

        harvest_job = toolkit.get_action('harvest_job_create')(
            context,
            {'source_id': harvest_source['id'], 'run': True})

        job_id = harvest_job['id']

        toolkit.get_action('harvest_jobs_run')(
            context,
            {'source_id': harvest_source['id']}
        )
        # assert harvest_job['source_id'] == harvest_source['id'], harvest_job
        # assert harvest_job['status'] == u'Running'

        harvest_job = toolkit.get_action('harvest_job_show')(
            context,
            {'id': job_id}
        )
        results = report._get_harvest_results()

        # test table_data_by_org
        assert organization['name'] in results['table_data_by_org'].keys()
        assert len(results['table_data_by_org'].keys()) == 1
        s1 = set(['organization_title', 'harvest_sources', 'total_datasets'])
        assert s1.issubset(results['table_data_by_org'][organization['name']].keys())
        assert results['table_data_by_org'][organization['name']
                                            ]['harvest_sources'] == 1
        assert results['table_data_by_org'][organization['name']
                                            ]['total_datasets'] == 0
        assert results['table_data_by_org'][organization['name']
                                            ]['organization_title'] == 'Test Organization'

        # test table data
        assert len(results['table']) == 1
        table = results['table'][0]
        assert table['name'] == 'test-source'
        assert table['source_type'] == 'datajson'
        assert table['state'] == 'active'
        assert table['frequency'] == 'MANUAL'
        assert table['organization_name'] == 'myorg'
        assert table['organization_title'] == 'Test Organization'
        assert table['job_count'] == 1
        assert table['total_datasets'] == 0

    def test_get_harvest_results_with_org(self, app):
        user = core_factories.Sysadmin(name='asdfs')
        organization = core_factories.Organization(name='myorg')
        source_dict = {
            'title': 'Test Source',
            'name': 'test-source',
            'url': 'raw.githubusercontent.com/GSA/catalog.data.gov/main/tests/harvest-sources/data.json',
            'frequency': "MANUAL",
            'source_type': 'datajson',
            'owner_org': organization['id']
        }

        context = {
            "model": model,
            "session": model.Session,
            "user": user['id']
        }
        try:
            harvest_source = toolkit.get_action('harvest_source_create')(
                context,
                source_dict)
            print('harvest source created')
        except toolkit.ValidationError:
            harvest_source = toolkit.get_action('harvest_source_show')(
                context,
                {'id': harvest_source['name']}
            )
            print('harvest source exists')

        harvest_job = toolkit.get_action('harvest_job_create')(
            context,
            {'source_id': harvest_source['id'], 'run': True})

        job_id = harvest_job['id']

        toolkit.get_action('harvest_jobs_run')(
            context,
            {'source_id': harvest_source['id']}
        )
        # assert harvest_job['source_id'] == harvest_source['id'], harvest_job
        # assert harvest_job['status'] == u'Running'

        harvest_job = toolkit.get_action('harvest_job_show')(
            context,
            {'id': job_id}
        )
        results = report._get_harvest_results(organization['name'])

        # test table_data_by_org
        assert organization['name'] in results['table_data_by_org'].keys()
        s1 = set(['organization_title', 'harvest_sources', 'total_datasets', 'packages'])
        assert s1.issubset(results['table_data_by_org'][organization['name']].keys())
        assert len(results['table_data_by_org'].keys()) == 1
        assert results['table_data_by_org'][organization['name']
                                            ]['harvest_sources'] == 1
        assert results['table_data_by_org'][organization['name']
                                            ]['total_datasets'] == 0
        assert results['table_data_by_org'][organization['name']
                                            ]['organization_title'] == 'Test Organization'

        # assert that table_data_by_org contains same entry as table
        TestCase().assertDictEqual(results['table_data_by_org']['myorg']['packages'][0],
                                   results['table'][0])

        # test table data
        assert len(results['table']) == 1
        table = results['table'][0]
        assert table['name'] == 'test-source'
        assert table['source_type'] == 'datajson'
        assert table['state'] == 'active'
        assert table['frequency'] == 'MANUAL'
        assert table['organization_name'] == 'myorg'
        assert table['organization_title'] == 'Test Organization'
        assert table['job_count'] == 1
        assert table['total_datasets'] == 0
