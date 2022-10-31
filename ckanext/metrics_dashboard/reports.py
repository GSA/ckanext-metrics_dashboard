import copy
import logging
from collections import OrderedDict, defaultdict

import ckan.model as model
import ckanext.harvest.model as harvest_model
import ckan.plugins as p
from ckanext.report import lib

log = logging.getLogger(__name__)


def metrics_dashboard(organization, include_sub_organizations=False):
    if organization is None:
        return metrics_dashboard_index(include_sub_organizations=include_sub_organizations)
    else:
        return metrics_dashboard_for_organization(organization=organization, include_sub_organizations=include_sub_organizations)


def metrics_dashboard_index(include_sub_organizations=False):
    print('>>>>>> metrics_dashboard_index')
    return _get_harvest_results()


def metrics_dashboard_for_organization(organization, include_sub_organizations=False):
    print('>>>>>> metrics_dashboard_for_organization')
    return _get_harvest_results()


def _get_harvest_results(organization=None):
    print('>>>>>> _get_harvest_results')
    table_data = []
    table_data_by_org = {}

    harvest_sources = model.Session.query(harvest_model.HarvestSource).all()

    # harvest_sources = model.Session.query(harvest_model.HarvestSource)\
    #     .filter(id == organization).all()   ### TODO: add filter query by org

    for source in harvest_sources:
        id = source.id
        context = {
            "model": model,
            "session": model.Session
        }
        source = p.toolkit.get_action("harvest_source_show")(
            context, {"id": id}
        )

        row_data = OrderedDict((
            ('name', source['name']),
            ('metadata_created', source['metadata_created']),
            ('source_type', source['source_type']),
            ('state', source['state']),
            ('frequency', source['frequency']),
            ('organization_name', source['organization']['name']),
            ('organization_title', source['organization']['title']),
            ('job_count', source['status']['job_count']),
            ('total_datasets', source['status']['total_datasets']),
            ('last_job_created', source['status']['last_job']['created']),
            ('last_job_finished', source['status']['last_job']['finished']),
            ('last_job_status', source['status']['last_job']['status']),
            ('last_job_added', source['status']['last_job']['stats']['added']),
            ('last_job_updated', source['status']['last_job']['stats']['updated']),
            ('last_job_not_modified', source['status']['last_job']['stats']['not modified']),
            ('last_job_errored', source['status']['last_job']['stats']['errored']),
            ('last_job_deleted', source['status']['last_job']['stats']['deleted']),
            ('object_error_summary', source['status']['last_job']['object_error_summary']),  # not yet implemented
        ))

        table_data.append(row_data)  # needed for csv export

        if (row_data['organization_name'] in table_data_by_org):
            table_data_by_org[row_data['organization_name']]['harvest_sources'] += 1
            table_data_by_org[row_data['organization_name']]['total_datasets'] += row_data['total_datasets']
            table_data_by_org[row_data['organization_name']]['packages'].append(row_data)
        else:
            table_data_by_org[row_data['organization_name']] = {
                'organization_title': row_data['organization_title'],
                'harvest_sources': 1,
                'total_datasets': row_data['total_datasets'],
                'packages': [row_data],
            }

    import ipdb
    ipdb.set_trace()
    return {
        'table': table_data,  # needed for csv export
        'table_data_by_org': table_data_by_org
    }


def metrics_dashboard_option_combinations():
    for organization in lib.all_organizations(include_none=True):
        for include_sub_organizations in (False, True):
            yield {'organization': organization,
                   'include_sub_organizations': include_sub_organizations}


metrics_dashboard_report_info = {
    'name': 'metrics-dashboard',
    'title': 'Metrics Dashboard',
    'description': 'Description here.',
    'option_defaults': OrderedDict((('organization', None),
                                    ('include_sub_organizations', False),
                                    )),
    'option_combinations': metrics_dashboard_option_combinations,
    'generate': metrics_dashboard,
    'template': 'report/metrics_dashboard.html',
}
