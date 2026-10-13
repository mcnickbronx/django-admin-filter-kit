# Changelog

## 0.2.0 — 2026-10-13

- Django 4.2 is supported.
- A subclass of `AutocompleteFilter` can set its own `title`; the default is still the field's name.
- `AutocompleteFilter.value()` returns the picked id — for subclasses with their own `queryset()`.

## 0.1.0 — 2026-10-13

- `AutocompleteFilter`: filter by a related object with search-as-you-type, built on the admin's
  autocomplete view.
- Collapsible filter sidebar, on by default; `ADMIN_FILTER_KIT_COLLAPSIBLE = False` turns it off.
- The cursor goes straight to the search box when a suggestion dropdown opens.
