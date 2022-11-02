import logging

import ckan.plugins as p
from ckan.plugins import toolkit
from ckanext.report.interfaces import IReport

log = logging.getLogger(__name__)

class MetricsDashboard(p.SingletonPlugin, p.toolkit.DefaultDatasetForm):
    """
    Registers to be notified whenever CKAN resources are created or their URLs
    change, and will create a new ckanext.archiver celery task to archive the
    resource.
    """
    p.implements(p.IDomainObjectModification, inherit=True)
    p.implements(IReport)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers)

    # IReport

    def register_reports(self):
        """Register details of an extension's reports"""
        from ckanext.metrics_dashboard import reports
        return [reports.metrics_dashboard_report_info,
                ]

    # IConfigurer

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')

    # IActions

    def get_actions(self):
        return {}
        return {
            'archiver_resource_show': action.archiver_resource_show,
            'archiver_dataset_show': action.archiver_dataset_show,
        }

    # IAuthFunctions
#
    def get_auth_functions(self):
        return {}
        return {
            'archiver_resource_show': auth.archiver_resource_show,
            'archiver_dataset_show': auth.archiver_dataset_show,
        }

    # ITemplateHelpers

    def get_helpers(self):
        return {}
        return dict((name, function) for name, function
                    in list(helpers.__dict__.items())
                    if callable(function) and name[0] != '_')
