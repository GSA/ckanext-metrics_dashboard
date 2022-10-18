import copy
try:
    from collections import OrderedDict  # from python 2.7
except ImportError:
    from sqlalchemy.util import OrderedDict

import ckan.model as model

from ckanext.report import lib


def metrics_dashboard(organization, include_sub_organizations=False):
    if organization is None:
        return metrics_dashboard_index(include_sub_organizations=include_sub_organizations)
    else:
        return metrics_dashboard_for_organization(organization=organization, include_sub_organizations=include_sub_organizations)


def metrics_dashboard_index(include_sub_organizations=False):
    orgs = model.Session.query(model.Group)\
        .filter(model.Group.type == 'organization')\
        .filter(model.Group.state == 'active').all()
    print(orgs)
    return {
        'table': [
            {'name': 'river-levels', 'title': 'River levels', 'notes': 'Harvested',
                'user': 'bob', 'created': '2008-06-13T10:24:59.435631'},
            {'name': 'co2-monthly', 'title': 'CO2 monthly', 'notes': '', 'user': 'bob', 'created': '2009-12-14T08:42:45.473827'},
        ],
        'num_packages': 56,
        'packages_without_tags_percent': 4,
        'average_tags_per_package': 3.5,
    }
    return {
        'table': data,
        'num_broken_packages': num_broken_packages,
        'num_broken_resources': num_broken_resources,
        'num_packages': num_packages,
        'num_resources': num_resources,
        'broken_package_percent': lib.percent(num_broken_packages, num_packages),
        'broken_resource_percent': lib.percent(num_broken_resources, num_resources),
    }


def metrics_dashboard_for_organization(organization, include_sub_organizations=False):
    return {
        'table': [
            {'name': 'river-levels', 'title': 'River levels', 'notes': 'Harvested',
                'user': 'bob', 'created': '2008-06-13T10:24:59.435631'},
            {'name': 'co2-monthly', 'title': 'CO2 monthly', 'notes': '', 'user': 'bob', 'created': '2009-12-14T08:42:45.473827'},
        ],
        'num_packages': 102,
        'packages_without_tags_percent': 4,
        'average_tags_per_package': 3.5,
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
