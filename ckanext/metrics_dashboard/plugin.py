import logging

import ckan.plugins as p
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

    # ITemplateHelpers

    def get_helpers(self):
        return {}
