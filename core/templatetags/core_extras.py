from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def gender_label(value):
    labels = {'M': 'Male', 'F': 'Female', 'O': 'Other'}
    return labels.get(value, '')
