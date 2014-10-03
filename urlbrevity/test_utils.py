# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from pytest import raises
from pytest import mark
from .errors import Decode404
from .errors import ContentType404
from .errors import Model404
from .utils import encode
from .utils import _reduced_alphabet
from .utils import decode
from .utils import get_encoded_object_or_404


def test_encode():
    assert encode(1, 2) == 'rQuX'


def test_decode():
    assert decode('rQuX') == (1, 2)


def test_reduced_alphabet():
    class StableTestAlphabet(object):
        ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # noqa
    assert _reduced_alphabet(StableTestAlphabet) == '-34679=FHQRUWXY_fhioqrsuwxy'  # noqa


def test_invalid_input_get_encoded_object_or_404():
    with raises(Decode404):
        get_encoded_object_or_404({'a': 1})


@mark.django_db
def test_invalid_decoded_content_type_get_encoded_object_or_404():
    enc = encode(99999, 1)
    with raises(ContentType404):
        get_encoded_object_or_404(enc)


@mark.django_db
def test_invalid_obj_get_encoded_object_or_404():
    ct = ContentType.objects.all()[0]
    enc = encode(ct.pk, 99999)
    with raises(Model404):
        get_encoded_object_or_404(enc)


@mark.django_db
def test_get_encoded_object_or_404():
    ct = ContentType.objects.get_for_model(User)
    user = User.objects.create()
    enc = encode(ct.pk, user.pk)
    obj = get_encoded_object_or_404(enc)
    assert obj == user
