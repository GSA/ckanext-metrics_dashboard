import copy
import logging
try:
    from collections import OrderedDict  # from python 2.7
except ImportError:
    from sqlalchemy.util import OrderedDict

import ckan.model as model
import ckanext.harvest.model as harvest_model
import ckan.plugins as p
from ckanext.report import lib

log = logging.getLogger(__name__)


def metrics_dashboard(organization, include_sub_organizations=False):
    print('>>>> metrics_dashboard')
    if organization is None:
        return metrics_dashboard_index(include_sub_organizations=include_sub_organizations)
    else:
        return metrics_dashboard_for_organization(organization=organization, include_sub_organizations=include_sub_organizations)


def metrics_dashboard_index(include_sub_organizations=False):
    print('>>>>>> metrics_dashboard_index')
    results = []
    total_datasets = 0
    harvest_sources = model.Session.query(harvest_model.HarvestSource).all()
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
            ('id', source['id']),
            ('metadata_created', source['metadata_created']),
            ('metadata_modified', source['metadata_modified']),
            ('organization_name', source['organization']['name']),
            ('job_count', source['status']['job_count']),
            ('total_datasets', source['status']['total_datasets']),
            ('last_job_created', source['status']['last_job']['created']),
            ('last_job_status', source['status']['last_job']['status']),
            ('last_job_added', source['status']['last_job']['stats']['added']),
            ('last_job_updated', source['status']['last_job']['stats']['updated']),
            ('last_job_not_modified', source['status']['last_job']['stats']['not modified']),
            ('last_job_errored', source['status']['last_job']['stats']['errored']),
            ('last_job_deleted', source['status']['last_job']['stats']['deleted']),
            ('last_job_order_error_summary', source['status']['last_job']['object_error_summary']),
        ))
        results.append(row_data)
        total_datasets += source['status']['total_datasets']

    return {
        'table': results,
        'total_datasets': total_datasets,
    }


def metrics_dashboard_for_organization(organization, include_sub_organizations=False):
    results = []
    total_datasets = 0
    harvest_sources = model.Session.query(harvest_model.HarvestSource).all()
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
            ('id', source['id']),
            ('metadata_created', source['metadata_created']),
            ('metadata_modified', source['metadata_modified']),
            ('organization_name', source['organization']['name']),
            ('job_count', source['status']['job_count']),
            ('total_datasets', source['status']['total_datasets']),
            ('last_job_created', source['status']['last_job']['created']),
            ('last_job_status', source['status']['last_job']['status']),
            ('last_job_added', source['status']['last_job']['stats']['added']),
            ('last_job_updated', source['status']['last_job']['stats']['updated']),
            ('last_job_not_modified', source['status']['last_job']['stats']['not modified']),
            ('last_job_errored', source['status']['last_job']['stats']['errored']),
            ('last_job_deleted', source['status']['last_job']['stats']['deleted']),
            ('last_job_order_error_summary', source['status']['last_job']['object_error_summary']),
        ))
        results.append(row_data)
        total_datasets += source['status']['total_datasets']
        # import ipdb
        # ipdb.set_trace()

    print('>>>>>> metrics_dashboard_for_organization')
    import ipdb
    ipdb.set_trace()

    return {
        'table': results,
        'total_datasets': total_datasets,
    }

    return {
        'organization_name': name,
        'organization_title': title,
        'num_broken_packages': num_broken_packages,
        'num_broken_resources': num_broken_resources,
        'num_packages': num_packages,
        'num_resources': num_resources,
        'broken_package_percent': lib.percent(num_broken_packages, num_packages),
        'broken_resource_percent': lib.percent(num_broken_resources, num_resources),
        'table': results
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
