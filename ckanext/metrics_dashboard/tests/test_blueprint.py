import pytest


@pytest.mark.ckan_config('ckan.plugins', 'metrics_dashboard')
@pytest.mark.use_fixtures('with_plugins', 'clean_db')
class TestMetricsDashboard():
    def test_metrics_base_url(self, app):
        response = app.get('/metrics')
        assert 'hello world!' in response.body

    def test_metrics_org_url(self, app):
        response = app.get('/metrics/ssa-gov')
        assert 'Your org is ssa-gov' in response.body
