from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplies the value by the argument
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter(name='sum')
def sum_filter(value, arg):
    """
    Adds the value and the argument
    """
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return ''

@register.filter(name='divide')
def divide(value, arg):
    """
    Divides the value by the argument
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter(name='sum_values')
def sum_values(value):
    """
    Returns the sum of the values in an iterable
    """
    try:
        return sum(float(v) for v in value)
    except (ValueError, TypeError):
        return 0