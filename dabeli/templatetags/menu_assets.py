import os

from django import template
from django.utils.text import slugify


register = template.Library()


@register.filter
def menu_image_url(value):
    """Return the canonical URL for both legacy and current menu records."""
    if not value:
        return ""

    filename = str(value).split("?", 1)[0].rsplit("/", 1)[-1]
    stem, _extension = os.path.splitext(filename)
    return f"/static/menu_assets/{slugify(stem)}.jpg"
