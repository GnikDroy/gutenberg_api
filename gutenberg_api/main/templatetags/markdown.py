from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
from markdown.extensions.toc import TocExtension as toc

register = template.Library()


@register.filter()
@stringfilter
def markdown(value, title="Table of Contents"):
    return md.markdown(value, extensions=[toc(title=title), 'extra', 'codehilite'])
