# -*- coding: utf-8 -*-
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory
from django.utils.encoding import force_text
from .utils import encode
from .signals import shortened_url
from .views import DoRedirect
from .views import DoInternalRedirect
from .views import do_redirect
from .views import do_internal_redirect
from .errors import View404
from pytest import mark
from pytest import raises


User.get_absolute_url = lambda self: '/test_user/{pk}/'.format(pk=self.pk)
LogEntry.get_absolute_url = lambda self: '/goes/nowhere/'


@mark.django_db(transaction=True)
def test_do_redirect():
    ct = ContentType.objects.get_for_model(User)
    user = User.objects.create()
    enc = encode(ct.pk, user.pk)
    request = RequestFactory().get('/')
    response = do_redirect(request=request, encoded_value=enc)
    assert response.status_code == 301
    assert response['Location'] == '/test_user/{0}/'.format(user.pk)


@mark.django_db(transaction=True)
def test_do_internal_redirect():
    ct = ContentType.objects.get_for_model(User)
    User.objects.create(username='test')
    user2 = User.objects.create(username='test2')
    enc = encode(ct.pk, user2.pk)
    request = RequestFactory().get('/')
    response = do_internal_redirect(request=request, encoded_value=enc)
    assert response.status_code == 200
    assert force_text(response.content) == force_text(user2.pk)


@mark.django_db(transaction=True)
def test_invalid_get_absolute_url_internal_redirect():
    ct = ContentType.objects.get_for_model(LogEntry)
    user = User.objects.create()
    entry = LogEntry.objects.create(user=user, action_flag=ADDITION)
    enc = encode(ct.pk, entry.pk)
    request = RequestFactory().get('/')
    with raises(View404):
        do_internal_redirect(request=request, encoded_value=enc)


@mark.django_db(transaction=True)
def test_cbv_do_redirect():
    ct = ContentType.objects.get_for_model(User)
    user = User.objects.create()
    enc = encode(ct.pk, user.pk)
    view = DoRedirect.as_view()
    request = RequestFactory().get('/')
    response = view(request=request, encoded_value=enc)
    assert response.status_code == 301
    assert response['Location'] == '/test_user/{0}/'.format(user.pk)


@mark.django_db(transaction=True)
def test_cbv_do_internal_redirect():
    ct = ContentType.objects.get_for_model(User)
    User.objects.create(username='test')
    user2 = User.objects.create(username='test2')
    enc = encode(ct.pk, user2.pk)
    view = DoInternalRedirect.as_view()
    request = RequestFactory().get('/')
    response = view(request=request, encoded_value=enc)
    assert response.status_code == 200
    assert force_text(response.content) == force_text(user2.pk)


@mark.django_db(transaction=True)
def test_cbv_invalid_get_absolute_url_internal_redirect():
    ct = ContentType.objects.get_for_model(LogEntry)
    user = User.objects.create()
    entry = LogEntry.objects.create(user=user, action_flag=ADDITION)
    enc = encode(ct.pk, entry.pk)
    view = DoInternalRedirect.as_view()
    request = RequestFactory().get('/')
    with raises(View404):
        view(request=request, encoded_value=enc)


@mark.django_db(transaction=True)
def test_signals():
    ct = ContentType.objects.get_for_model(User)
    user = User.objects.create()
    enc = encode(ct.pk, user.pk)
    request = RequestFactory().get('/')

    expecting_kwargs = {}

    def listener(*args, **kwargs):
        if 'signal' in kwargs:
            kwargs.pop('signal')
        expecting_kwargs.update(**kwargs)  # leak into above scope please.
        return LogEntry.objects.create(user=kwargs['instance'],
                                       action_flag=ADDITION)

    shortened_url.connect(listener, sender=User, dispatch_uid="test")
    do_redirect(request=request, encoded_value=enc)
    shortened_url.disconnect(listener, sender=User)
    assert len(expecting_kwargs) == 6
    assert expecting_kwargs == {
        'decoded': (ct.pk, user.pk),
        'encoded': enc,
        'instance': user,
        'sender': User,
        'content_type': ct,
        'url': '/test_user/{0}/'.format(user.pk),
    }
    assert LogEntry.objects.count() == 1
