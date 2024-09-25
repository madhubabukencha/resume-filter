"""
Here you can create your own filter that you can use in
your django templates.

To use the filter in your templates you have to load them
like below on the top of templates document:
{% load custom_filters %}
"""
import re
from django import template

register = template.Library()


@register.filter
def extract_email(value):
    """Extracts email addresses from the given text."""
    email_pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+)"
    matches = re.findall(email_pattern, value)
    if matches:
        return matches[0]  # return the first email found (as per your example)
    return ''
