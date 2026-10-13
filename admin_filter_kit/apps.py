from django.apps import AppConfig, apps
from django.core import checks


class AdminFilterKitConfig(AppConfig):
    name = "admin_filter_kit"
    verbose_name = "Admin filter kit"

    def ready(self):
        checks.register(check_app_order, checks.Tags.templates)


def check_app_order(app_configs, **kwargs):
    """The kit's admin/change_list.html wins over Django's only when the app is listed first."""
    name_list = [config.name for config in apps.get_app_configs()]
    if "django.contrib.admin" in name_list and name_list.index("admin_filter_kit") > name_list.index("django.contrib.admin"):
        return [
            checks.Warning(
                '"admin_filter_kit" is listed after "django.contrib.admin" in INSTALLED_APPS, '
                "so its changelist template is not used and AutocompleteFilter gets no scripts.",
                hint='Move "admin_filter_kit" above "django.contrib.admin".',
                id="admin_filter_kit.W001",
            )
        ]
    return []
