from django import forms
from django.contrib import admin
from django.contrib.admin.utils import get_model_from_relation
from django.contrib.admin.widgets import AutocompleteSelect


class AutocompleteFilter(admin.RelatedFieldListFilter):
    """Changelist filter by a related object, picked with search-as-you-type.

    Usage: ``list_filter = [("author", AutocompleteFilter)]``. Options come from the admin's own
    autocomplete view, so the related model's admin needs ``search_fields`` — the same rule as for
    ``autocomplete_fields``. The related table is never loaded as a whole: only the selected object.

    A subclass may set its own ``title`` and override ``queryset()``, reading the picked id with ``value()``.
    """

    template = "admin_filter_kit/autocomplete_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.title = type(self).title or self.title  # the parent class always takes the field's name
        self.form_field = forms.ModelChoiceField(
            queryset=get_model_from_relation(field)._default_manager.all(),
            to_field_name=field.target_field.attname,
            required=False,
            widget=AutocompleteSelect(field, model_admin.admin_site, attrs={"data-width": "100%"}),
        )

    def value(self):
        """The picked id as a string, or None."""
        value = self.lookup_val
        if isinstance(value, list):  # Django 5.0+ keeps every value of the parameter
            value = value[-1] if value else None
        return value

    def field_choices(self, field, request, model_admin):
        return []  # the parent class would load every related object here

    def has_output(self):
        return True

    @property
    def media(self):
        """Select2 and the filter script — added to the changelist by the kit's change_list.html."""
        return self.form_field.widget.media + forms.Media(
            css={"all": ["admin_filter_kit/autocomplete_filter.css"]},
            # jquery.init.js is listed for the order only: the script needs django.jQuery
            js=["admin/js/jquery.init.js", "admin_filter_kit/autocomplete_filter.js"],
        )

    def choices(self, changelist):
        # One "choice" for the template: the widget and the list address without this filter
        yield {
            "widget": self.form_field.widget.render(self.lookup_kwarg, self.value()),
            "query_string": changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            "lookup_kwarg": self.lookup_kwarg,
        }
