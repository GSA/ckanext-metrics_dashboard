import logging

import ckan.plugins as p
from ckan.plugins import toolkit

from . import blueprint


log = logging.getLogger(__name__)


class MetricsDashboard(p.SingletonPlugin):
    p.implements(p.IBlueprint)

    def get_blueprint(self):
        return blueprint.metrics_bp
