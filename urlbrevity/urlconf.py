# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import do_redirect
from .views import do_internal_redirect
from .utils import REDUCED_ALPHABET

ALPHABET_REGEX = r'^(?P<{kw}>[{chars}]+)/?$'.format(kw='encoded_value',
                                                    chars=REDUCED_ALPHABET)


redirect_url = url(
    regex=ALPHABET_REGEX,
    view=do_redirect,
    name="short",
)

internal_redirect_url = url(
    regex=ALPHABET_REGEX,
    view=do_internal_redirect,
    name="short",
)


def _generated_urlpatterns(redirects=False):
    """
    usage ... well, it probably works:
    import urlbrevity
    include(urlbrevity.urlconf.urls(redirects=True))
    """
    if redirects is True:
        _urls = (redirect_url,)
    else:
        _urls = (internal_redirect_url,)
    return (_urls, 'urlbrevity', 'urlbrevity')


redirects = _generated_urlpatterns(redirects=True)
no_redirects = _generated_urlpatterns(redirects=False)
