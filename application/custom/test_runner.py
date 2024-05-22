from django.test.runner import DiscoverRunner

class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # os.environ['DJANGO_SETTINGS_MODULE'] = 'application.settings_for_test'
        return super().setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        super().teardown_databases(old_config, **kwargs)

