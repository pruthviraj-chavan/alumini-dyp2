from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    """Add a CSS class to a Django form field"""
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css_class})
    return field
