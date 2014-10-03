# -*- coding: utf-8 -*-
from pytest import raises
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import Resolver404
from django.http import HttpResponse
import urlbrevity

try:
    from django.conf.urls import patterns, url, include
except ImportError:  # pragma: no cover
    from django.conf.urls.defaults import patterns, url, include
finally:
    def just_a_view(request, pk):
        return HttpResponse(str(pk))

    urlpatterns = patterns("",
        url(regex=r'^test_user/(?P<pk>\d+)/?$',
            view=just_a_view),
        url(r'redirect/', include(urlbrevity.redirects)),
        url(r'admin/', include(admin.site.urls)),
    )


def test_reversing():
    assert (reverse('urlbrevity:short', kwargs={'encoded_value': 'rQuX'})
            == '/redirect/rQuX')


def test_reversing_badchars():
    with raises(NoReverseMatch):
        reverse('urlbrevity:short', kwargs={'encoded_value': 'rQu1'})


def test_resolving():
    assert resolve('/redirect/rQuX').func == urlbrevity.do_redirect


def test_resolving_badchars():
    with raises(Resolver404):
        resolve('/redirect/rQu1')
