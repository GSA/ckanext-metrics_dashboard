import logging
from flask import Blueprint
import ckan.plugins as p

import ckanext.metrics_dashboard.utils as utils

log = logging.getLogger(__name__)


def get_all_metrics():
    return "hello world!"


def get_metrics_by_org(org):
    return utils.get_metrics_by_org(org)


class MetricsDashboard(p.SingletonPlugin):
    p.implements(p.IBlueprint)

    def get_blueprint(self):
        blueprint = Blueprint('metrics', self.__module__)
        rules = [
            ('/metrics', 'get_metrics', get_all_metrics),
            ('/metrics/<org>', 'get_metrics_by_org', get_metrics_by_org)
        ]

        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint
