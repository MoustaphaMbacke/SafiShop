from django import template
from django.core.files.storage import default_storage

register = template.Library()


@register.filter(name='storage_url')
def storage_url(value):
    """
    Given a FieldFile or a name string, return the URL according to the current
    DEFAULT_FILE_STORAGE. If value is falsy, return empty string.
    Usage in templates:
      {{ obj.image|storage_url }}
      {{ obj.image.name|storage_url }}
    """
    if not value:
        return ''
    # FieldFile objects have a 'name' attribute
    name = getattr(value, 'name', None) or value

    try:
        return default_storage.url(name)
    except Exception:
        # Fall back to name or empty string on error
        try:
            return name or ''
        except Exception:
            return ''
