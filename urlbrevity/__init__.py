# -*- coding: utf-8 -*-
# this is our public API.
from .urlconf import redirect_url
from .urlconf import internal_redirect_url
from .urlconf import redirects
from .urlconf import no_redirects

from .errors import Decode404
from .errors import Model404
from .errors import ContentType404
from .errors import View404

from .utils import encode
from .utils import decode
from .utils import get_encoded_object_or_404
from .utils import encode_model_instance
from .utils import decode_model_instance
from .utils import short_url
from .utils import ShortUrl

from .signals import shortened_url

from .views import do_redirect
from .views import do_internal_redirect

from .sitemaps import ShortUrlSitemap
from .feeds import ShortUrlFeed


__all__ = (
    'redirect_url',
    'internal_redirect_url',
    'redirects',
    'no_redirects',

    'Decode404',
    'Model404',
    'ContentType404',
    'View404',

    'encode',
    'decode',
    'get_encoded_object_or_404',
    'encode_model_instance',
    'decode_model_instance',
    'short_url',
    'ShortUrl',

    'shortened_url',

    'do_redirect',
    'do_internal_redirect',

    'ShortUrlSitemap',
    'ShortUrlFeed',
)
