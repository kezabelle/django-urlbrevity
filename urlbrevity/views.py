# -*- coding: utf-8 -*-
import logging
from django.http import HttpResponsePermanentRedirect
from .utils import get_encoded_object_or_404
from .errors import View404
from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import redirect
from django.utils.http import is_safe_url
from django.views.decorators.http import require_safe
from django.views.generic import View


logger = logging.getLogger(__name__)


def _get_obj_url(request, obj):
    try:
        url = obj.get_absolute_url()
    except AttributeError:
        msg = ("This model instance doesn't have an implementation of "
               "get_absolute_url")
        logger.error(msg, exc_info=1, extra={'request': request, 'status': 404})
        raise View404(msg)
    if not url:
        raise View404("Empty url to redirect to")
    if not is_safe_url(url):
        raise View404("Unsafe redirection")
    return url


def _resolve_and_call(request, url):
    try:
        callback, callback_args, callback_kwargs = resolve(url)
    except Resolver404:
        msg = ("Unable to call any function for `{url!s}` because no "
               "urlpattern was found".format(url=url))
        logger.error(msg, exc_info=1, extra={'request': request, 'status': 404})
        raise View404(msg)
    return callback(request, *callback_args, **callback_kwargs)


@require_safe
def do_redirect(request, encoded_value):
    instance = get_encoded_object_or_404(encoded_value)
    url = _get_obj_url(request=request, obj=instance)
    return HttpResponsePermanentRedirect(redirect_to=url)


@require_safe
def do_internal_redirect(request, encoded_value):
    """
    We don't allow unsafe request methods, because this isn't the canonical
    URL to point to.
    """
    instance = get_encoded_object_or_404(encoded_value)
    url = _get_obj_url(request=request, obj=instance)
    return _resolve_and_call(request=request, url=url)


################################################################################
# Here be class based views, if you need to extend stuff.
# Gosh how I hate them.
################################################################################


class DoRedirect(View):
    http_method_names = ['get', 'head']

    def get_object(self):
        return get_encoded_object_or_404(self.kwargs['encoded_value'])

    def get_absolute_url(self):
        return _get_obj_url(request=self.request, obj=self.object)

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        self.url = self.get_absolute_url()
        return self.render_to_response()

    def render_to_response(self):
        return HttpResponsePermanentRedirect(redirect_to=self.url)


class DoInternalRedirect(DoRedirect):
    def render_to_response(self):
        return _resolve_and_call(request=self.request, url=self.url)
