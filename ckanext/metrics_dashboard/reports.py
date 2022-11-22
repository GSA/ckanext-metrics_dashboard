import logging
from collections import OrderedDict

import ckan.model as model
import ckanext.harvest.model as harvest_model
import ckan.plugins as p

log = logging.getLogger(__name__)


def metrics_dashboard(organization=None, include_sub_organizations=False):
    if organization is None:
        return metrics_dashboard_index(include_sub_organizations=include_sub_organizations)
    else:
        return metrics_dashboard_for_organization(organization=organization,
                                                  include_sub_organizations=include_sub_organizations)


def metrics_dashboard_index(include_sub_organizations=False):
    return _get_harvest_results()


def metrics_dashboard_for_organization(organization, include_sub_organizations=False):
    return _get_harvest_results(organization)


def _get_harvest_results(organization=None):
    table_data = []
    table_data_by_org = {}

    context = {
        "model": model,
        "session": model.Session
    }

    query = model.Session.query(harvest_model.HarvestSource)

    if organization:
        # if passed an organization, we need to fetch the org id
        org = p.toolkit.get_action("organization_show")(
            context, {"id": organization}
        )
        # filter harvest source query by org id
        query = query.join(
            model.Package, harvest_model.HarvestSource.id == model.Package.id
        ).filter(model.Package.owner_org == org['id']).all()

    else:
        # get all harvest sources
        query = query.all()

    for source in query:
        id = source.id
        try:
            source = p.toolkit.get_action("harvest_source_show")(
                context, {"id": id}
            )

            last_job = source['status']['last_job']
            source_org = source['organization']
            if not last_job:
                last_job = {
                    'created': 'N/A',
                    'finished': 'N/A',
                    'status': 'N/A',
                    'stats': {
                        'added': 'N/A',
                        'updated': 'N/A',
                        'not modified': 'N/A',
                        'errored': 'N/A',
                        'deleted': 'N/A',
                    },
                    'object_error_summary': 'N/A',
                }
            if not source_org:
                source_org = {
                    'name': 'N/A',
                    'title': 'N/A',
                }
            row_data = OrderedDict((
                ('name', source['name']),
                ('metadata_created', source['metadata_created']),
                ('source_type', source['source_type']),
                ('state', source['state']),
                ('frequency', source['frequency']),
                ('organization_name', source_org['name']),
                ('organization_title', source_org['title']),
                ('job_count', source['status']['job_count']),
                ('total_datasets', source['status']['total_datasets']),
                ('last_job_created', last_job['created']),
                ('last_job_finished', last_job['finished']),
                ('last_job_status', last_job['status']),
                ('last_job_added', last_job['stats']['added']),
                ('last_job_updated', last_job['stats']['updated']),
                ('last_job_not_modified', last_job['stats']['not modified']),
                ('last_job_errored', last_job['stats']['errored']),
                ('last_job_deleted', last_job['stats']['deleted']),
                ('object_error_summary', last_job['object_error_summary']),  # not yet implemented
            ))

            table_data.append(row_data)  # needed for csv export

            if (row_data['organization_name'] in table_data_by_org):
                table_data_by_org[row_data['organization_name']]['harvest_sources'] += 1
                table_data_by_org[row_data['organization_name']]['total_datasets'] += row_data['total_datasets']
                # if we have an org, append the source data
                if organization:
                    table_data_by_org[row_data['organization_name']]['packages'].append(row_data)
            else:
                table_data_by_org[row_data['organization_name']] = {
                    'organization_title': row_data['organization_title'],
                    'harvest_sources': 1,
                    'total_datasets': row_data['total_datasets'],
                }
                # if we have an org, append the source data
                if organization:
                    table_data_by_org[row_data['organization_name']]['packages'] = [row_data]
        except BaseException as exception:
            logging.exception(
                f"An exception was thrown: {exception} ... While trying to process harvest source: {source.id} ")
            continue
            # some datasets error out and default to an internal url.
            # TODO: process these datasets with authorization errors into a separate table

    return {
        'table': table_data,  # needed for csv export
        'table_data_by_org': table_data_by_org
    }


metrics_dashboard_report_info = {
    'name': 'metrics-dashboard',
    'title': 'Metrics Dashboard',
    'description': 'A dashboard to report harvest source metrics by organization.',
    'option_defaults': OrderedDict((('organization', None),
                                    ('include_sub_organizations', False),
                                    )),
    'option_combinations': None,
    'generate': metrics_dashboard,
    'template': 'report/metrics_dashboard.html',
}
