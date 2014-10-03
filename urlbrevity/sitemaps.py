# -*- coding: utf-8 -*-
from itertools import chain
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from .utils import encode_model_instance


class ShortUrlSitemap(Sitemap):
    models = ()

    def get_models(self):
        return self.models

    def get_querysets(self):
        for model in self.get_models():
            yield model.objects.filter()

    def items(self):
        return tuple(chain.from_iterable(self.get_querysets()))

    def location(self, obj):
        encoded = encode_model_instance(obj)
        return reverse('urlbrevity:short', kwargs={'encoded_value': encoded})
