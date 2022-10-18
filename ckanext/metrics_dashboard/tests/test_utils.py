import ckanext.metrics_dashboard.utils as utils


def test_get_metrics_by_org():
    org = 'ssa-gov'
    res = utils.get_metrics_by_org(org)

    assert res == f"Your org is {org}"
