# -*- coding: utf-8 -*-
from .utils import short_url


class ShortUrlFeed(object):
    """
    A mixin for including into Feed subclasses to use short URLs instead
    """
    def item_link(self, obj):
        return short_url(obj)
