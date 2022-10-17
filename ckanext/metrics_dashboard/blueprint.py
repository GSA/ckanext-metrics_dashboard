import logging
from flask import Blueprint

import ckanext.metrics_dashboard.utils as utils

log = logging.getLogger(__name__)

metrics_bp = Blueprint('datajson', __name__)


def get_all_metrics():
    return "hello world!"


def get_metrics_by_org(org):
    return utils.get_metrics_by_org(org)


metrics_bp.add_url_rule('/metrics', 'get_metrics',
                        get_all_metrics)
metrics_bp.add_url_rule('/metrics/<org>', 'get_metrics_by_org',
                        get_metrics_by_org)
