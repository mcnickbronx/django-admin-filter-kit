from django import forms, template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def filter_kit_media(context):
    """The changelist ``media`` plus the kit's scripts and styles.

    Merged into Django's own media rather than printed next to it: Django then keeps the script
    order (Select2 must load before jquery.init.js) and, in Django 6.0+, adds the CSP nonce.
    """
    media = context.get("media") or forms.Media()
    changelist = context.get("cl")
    for spec in getattr(changelist, "filter_specs", []):
        spec_media = getattr(spec, "media", None)
        if isinstance(spec_media, forms.Media):
            media += spec_media
    if getattr(changelist, "has_filters", False) and getattr(settings, "ADMIN_FILTER_KIT_COLLAPSIBLE", True):
        media += forms.Media(css={"all": ["admin_filter_kit/collapse.css"]}, js=["admin_filter_kit/collapse.js"])
    return media
