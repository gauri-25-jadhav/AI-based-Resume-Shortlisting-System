from django import template

register = template.Library()

@register.filter
def split(value, key=","):
    if value:
        return [item.strip() for item in value.split(key)]
    return []
