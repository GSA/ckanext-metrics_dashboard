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
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IPackageController, inherit=True)

    # p.implements(p.IClick)

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

    # IPackageController

    # def after_show(self, context, pkg_dict):
    #     """ Old CKAN function name """
    #     return self.after_dataset_show(context, pkg_dict)

    # def after_dataset_show(self, context, pkg_dict):
    #     # Insert the archival info into the package_dict so that it is
    #     # available on the API.
    #     # When you edit the dataset, these values will not show in the form,
    #     # it they will be saved in the resources (not the dataset). I can't see
    #     # and easy way to stop this, but I think it is harmless. It will get
    #     # overwritten here when output again.
    #     archivals = Archival.get_for_package(pkg_dict['id'])
    #     if not archivals:
    #         return

    #     # dataset
    #     dataset_archival = aggregate_archivals_for_a_dataset(archivals)
    #     pkg_dict['archiver'] = dataset_archival

    #     # resources
    #     archivals_by_res_id = dict((a.resource_id, a) for a in archivals)
    #     for res in pkg_dict['resources']:
    #         archival = archivals_by_res_id.get(res['id'])
    #         if archival:
    #             archival_dict = archival.as_dict()
    #             del archival_dict['id']
    #             del archival_dict['package_id']
    #             del archival_dict['resource_id']
    #             res['archiver'] = archival_dict

    # def before_dataset_index(self, pkg_dict):
    #     '''
    #     remove `archiver` from index
    #     '''
    #     pkg_dict.pop('archiver', None)
    #     return pkg_dict

    # # IClick

    # def get_commands(self):
    #     return cli.get_commands()
