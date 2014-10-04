# -*- coding: utf-8 -*-
from django.dispatch import Signal


shortened_url = Signal(providing_args=["instance", "url", "content_type",
                                       "encoded", "decoded"])
