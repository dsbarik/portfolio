import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_filter(text):
    """
    Convert markdown text to HTML.
    Usage: {{ variable|markdown }}
    """
    return mark_safe(md.markdown(text, extensions=["extra", "nl2br"]))


@register.filter(name="is_list")
def is_list(value):
    """Check if value is a list"""
    return isinstance(value, list)


@register.filter(name="prettify")
def prettify(value):
    """Convert snake_case key to Title Case"""
    return value.replace("_", " ").title()
