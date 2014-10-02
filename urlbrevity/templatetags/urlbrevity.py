# -*- coding: utf-8 -*-
import logging
from django import template
from ..utils import encode_model_instance


register = template.Library()
logger = logging.getLogger(__name__)


@register.filter(name='hashid', is_safe=True)
def convert_model_instance_to_hashid(value):
    if not value:
        logger.warning("No useful input")
        return ''
    encoded = encode_model_instance(obj=value)
    if encoded is None:
        return ''
    return encoded
