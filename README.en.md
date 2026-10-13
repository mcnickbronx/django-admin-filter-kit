# django-admin-filter-kit

[![PyPI](https://img.shields.io/pypi/v/django-admin-filter-kit)](https://pypi.org/project/django-admin-filter-kit/)
[![Python](https://img.shields.io/pypi/pyversions/django-admin-filter-kit)](https://pypi.org/project/django-admin-filter-kit/)
[![Django](https://img.shields.io/pypi/frameworkversions/django/django-admin-filter-kit)](https://pypi.org/project/django-admin-filter-kit/)
[![Tests](https://github.com/mcnickbronx/django-admin-filter-kit/actions/workflows/tests.yml/badge.svg)](https://github.com/mcnickbronx/django-admin-filter-kit/actions/workflows/tests.yml)

[Русский](https://github.com/mcnickbronx/django-admin-filter-kit/blob/main/README.md) · English

Small additions to the filters of Django admin lists:

- **`AutocompleteFilter`** — filter by a related object with search-as-you-type, for related
  tables too big for a list of links in the sidebar.
- **Collapsible filter sidebar** — a click on the "Filter" heading hides the filters and gives
  the table the full width. The browser remembers the choice for all lists. On by default.
- **The cursor goes straight to the search box** when a suggestion dropdown opens. Select2 4.0.13,
  bundled with Django, doesn't focus it with jQuery 3.6+, and the first typed letter is lost.

On PyPI: `pip install django-admin-filter-kit`. No dependencies besides Django.
Supports Django 4.2, 5.2, 6.0 and 6.1 on Python 3.10+.

## Installation

```
pip install django-admin-filter-kit
```

```python
INSTALLED_APPS = [
    "admin_filter_kit",  # above django.contrib.admin
    "django.contrib.admin",
    # ...
]
```

The app must come before `django.contrib.admin`: it adds its scripts through its own
`admin/change_list.html`, which extends Django's, and Django uses the first template it finds.
If the order is wrong, the system check `admin_filter_kit.W001` says so.

## Autocomplete filter

```python
from django.contrib import admin

from admin_filter_kit.filters import AutocompleteFilter


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = [
        ("author", AutocompleteFilter),        # ForeignKey
        ("tags", AutocompleteFilter),          # ManyToManyField
        ("author__country", AutocompleteFilter),  # across relations
    ]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]  # required: suggestions search these fields
```

Suggestions come from the admin's own autocomplete view — the one behind `autocomplete_fields`.
So there are no extra URLs, and the rules are the same:

- the related model's admin must have `search_fields`;
- suggestions are shown to users who can view the related model, with its admin's search,
  ordering and the field's `limit_choices_to`;
- they load in pages of 20 while you type and scroll; labels are `str(obj)`.

The list page never loads the related table: only the selected object, to show its name.
Picking an object reloads the list filtered by it, the × clears the filter. Other filters,
search and ordering stay as they are.

The filter's title is the field's name by default. A subclass sets its own title and its own
filtering; `value()` returns the picked object's id or `None`.

```python
class CompanyFilter(AutocompleteFilter):
    title = "company"

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        # e.g. a document is linked to a company through either of two tables
        return queryset.filter(Q(act__company=self.value()) | Q(invoice__company=self.value())).distinct()


list_filter = [("act__company", CompanyFilter)]  # suggestions come from the act.company field
```

Not supported yet: several objects at once and a choice for records without a related object.

## Collapsible sidebar

Works on every admin list with filters, no code needed. To turn it off:

```python
ADMIN_FILTER_KIT_COLLAPSIBLE = False
```

## Custom changelist templates

If a project overrides `admin/change_list.html`, or a `ModelAdmin` sets
`change_list_template`, that template must extend `"admin/change_list.html"` — the usual way.
Otherwise the kit's scripts are not added to the page, and the autocomplete filter doesn't work.

## Development

```
pip install -e .
python -m django test --settings=tests.settings
```

## License

MIT
