# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from .utils import encode_model_instance


class ShortUrlFeed(object):
    """
    A mixin for including into Feed subclasses to use short URLs instead
    """
    def item_link(self, obj):
        encoded = encode_model_instance(obj=obj)
        return reverse('urlbrevity:short', kwargs={'encoded_value': encoded})
