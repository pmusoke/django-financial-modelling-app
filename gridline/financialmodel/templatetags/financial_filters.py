from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def percentage(value):
    if value is None:
        return ""
    
    return f"{value * 100:.2f}%"

@register.filter
def currency_format(value):
    try:
        number = Decimal(str(value))

        if round(number, 2) == 0:
            return "0.00"
        
        return f"{number:,.2f}"
    
    except (InvalidOperation, ValueError, TypeError):
        return value


@register.filter
def ratio_format(value):

    if value is None:
        return "N/A"

    if value == "N/A":
        return "N/A"

    try:
        return f"{float(value):.4f}"
    except(ValueError, TypeError):
        return value
