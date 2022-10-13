import logging
from flask import Blueprint
import ckan.plugins as p

log = logging.getLogger(__name__)


def get_metrics():
    return "Hello World!"


class MetricsDashboard(p.SingletonPlugin):
    p.implements(p.IBlueprint)

    def get_blueprint(self):
        blueprint = Blueprint('metrics', self.__module__)
        rules = [
            ('/metrics', 'get_metrics', get_metrics)
        ]

        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint
