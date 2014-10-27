# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from pytest import raises
from pytest import mark
from .errors import Decode404
from .errors import ContentType404
from .errors import Model404
from .utils import encode
from .utils import encode_model_instance
from .utils import _reduced_alphabet
from .utils import decode
from .utils import get_encoded_object_or_404
from .utils import short_url
from .utils import ShortUrl


def test_encode():
    assert encode(1, 2) == 'oyuw'


def test_decode():
    assert decode('oyuw') == (1, 2)


def test_reduced_alphabet():
    class StableTestAlphabet(object):
        ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # noqa
    assert _reduced_alphabet(StableTestAlphabet) == '34679FHQRUWXYfhioqrsuwxy'


def test_invalid_input_get_encoded_object_or_404():
    with raises(Decode404):
        get_encoded_object_or_404({'a': 1})


@mark.django_db(transaction=True)
def test_invalid_decoded_content_type_get_encoded_object_or_404():
    enc = encode(99999, 1)
    with raises(ContentType404):
        get_encoded_object_or_404(enc)


@mark.django_db(transaction=True)
def test_invalid_obj_get_encoded_object_or_404():
    ct = ContentType.objects.all()[0]
    enc = encode(ct.pk, 99999)
    with raises(Model404):
        get_encoded_object_or_404(enc)


@mark.django_db(transaction=True)
def test_get_encoded_object_or_404():
    ct = ContentType.objects.get_for_model(User)
    user = User.objects.create()
    enc = encode(ct.pk, user.pk)
    encoded_obj = get_encoded_object_or_404(enc)
    assert encoded_obj.obj == user


def test_encode_instance_no_absolute_url():
    class PretendModel(object):
        pk = 1
    enc = encode_model_instance(PretendModel())
    assert enc is None


@mark.django_db(transaction=True)
def test_shorturl_descriptor():
    class UserProxy(User):
        short_url = ShortUrl()

        class Meta:
            proxy = True

    user = UserProxy.objects.create()
    assert user.short_url == short_url(user)
    with raises(NotImplementedError):
        user.short_url = 'test'


def test_short_url_may_return_none():
    class PretendModel(object):
        pk = 1
    result = short_url(PretendModel())
    assert result is None
