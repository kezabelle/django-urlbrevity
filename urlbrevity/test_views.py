# -*- coding: utf-8 -*-
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory
from urlbrevity.utils import encode
from .views import DoRedirect
from .views import DoInternalRedirect
from .views import do_redirect
from .views import do_internal_redirect
from .errors import View404
from pytest import mark
from pytest import raises


User.get_absolute_url = lambda self: '/test_user/{pk}/'.format(pk=self.pk)
LogEntry.get_absolute_url = lambda self: '/goes/nowhere/'


@mark.django_db
def test_do_redirect():
    ct = ContentType.objects.get_for_model(User)
    user = User.objects.create()
    enc = encode(ct.pk, user.pk)
    request = RequestFactory().get('/')
    response = do_redirect(request=request, encoded_value=enc)
    assert response.status_code == 301
    assert response['Location'] == '/test_user/1/'


@mark.django_db
def test_do_internal_redirect():
    ct = ContentType.objects.get_for_model(User)
    User.objects.create(username='test')
    user2 = User.objects.create(username='test2')
    enc = encode(ct.pk, user2.pk)
    request = RequestFactory().get('/')
    response = do_internal_redirect(request=request, encoded_value=enc)
    assert response.status_code == 200
    assert response.content == str(user2.pk)


@mark.django_db
def test_invalid_get_absolute_url_internal_redirect():
    ct = ContentType.objects.get_for_model(LogEntry)
    user = User.objects.create()
    entry = LogEntry.objects.create(user=user, action_flag=ADDITION)
    enc = encode(ct.pk, entry.pk)
    request = RequestFactory().get('/')
    with raises(View404):
        do_internal_redirect(request=request, encoded_value=enc)


@mark.django_db
def test_cbv_do_redirect():
    ct = ContentType.objects.get_for_model(User)
    user = User.objects.create()
    enc = encode(ct.pk, user.pk)
    view = DoRedirect.as_view()
    request = RequestFactory().get('/')
    response = view(request=request, encoded_value=enc)
    assert response.status_code == 301
    assert response['Location'] == '/test_user/1/'


@mark.django_db
def test_cbv_do_internal_redirect():
    ct = ContentType.objects.get_for_model(User)
    User.objects.create(username='test')
    user2 = User.objects.create(username='test2')
    enc = encode(ct.pk, user2.pk)
    view = DoInternalRedirect.as_view()
    request = RequestFactory().get('/')
    response = view(request=request, encoded_value=enc)
    assert response.status_code == 200
    assert response.content == str(user2.pk)


@mark.django_db
def test_cbv_invalid_get_absolute_url_internal_redirect():
    ct = ContentType.objects.get_for_model(LogEntry)
    user = User.objects.create()
    entry = LogEntry.objects.create(user=user, action_flag=ADDITION)
    enc = encode(ct.pk, entry.pk)
    view = DoInternalRedirect.as_view()
    request = RequestFactory().get('/')
    with raises(View404):
        view(request=request, encoded_value=enc)
