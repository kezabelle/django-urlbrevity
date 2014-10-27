# -*- coding: utf-8 -*-
import logging
from django import template
from django.core.urlresolvers import NoReverseMatch
from ..utils import encode_model_instance
from ..utils import short_url


register = template.Library()
logger = logging.getLogger(__name__)


@register.filter(name='hashid', is_safe=True)
def convert_model_instance_to_hashid(value):
    if not value:  # pragma: no cover
        logger.warning("No useful input")
        return ''
    encoded = encode_model_instance(obj=value)
    if encoded is None:  # pragma: no cover
        return ''
    return encoded.hash


@register.filter(name='short_url')
def convert_model_instance_to_url(value):
    if not value:  # pragma: no cover
        logger.warning("No useful input")
        return ''
    try:
        url = short_url(value)
    except NoReverseMatch:  # pragma: no cover
        return ''
    if url is None:
        return ''
    return url
