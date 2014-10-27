# -*- coding: utf-8 -*-
from collections import namedtuple
import logging
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import DatabaseError
from django.http import Http404
from hashids import Hashids
from django.conf import settings
from .errors import Decode404
from .errors import ContentType404
from .errors import Model404


logger = logging.getLogger(__name__)


def _reduced_alphabet(cls):
    """
    we now configure the alphabet available to remove lookalike and
    soundalike characters
    """
    base_alphabet = frozenset(cls.ALPHABET)
    # 1 = l, L, I
    # 2 = Z; 5 = S; 8 = B; 0 = O
    numbers = frozenset('12580')
    # also remove the letters that could be confused for numbers.
    letters_numbers = frozenset('lL I Zz S B O')
    # these may all sound like "ee"
    ee_letters = frozenset('bcdegptvz BCDEGPTVZ')
    # these may sound like "a"
    aa_letters = frozenset('ajk AJK')
    # these sound like "m"
    m_letters = frozenset('mn MN')

    alphabet = (base_alphabet - letters_numbers - numbers -
                ee_letters - aa_letters - m_letters)
    logger.debug("available alphabet is: {0!r}".format(alphabet))
    return ''.join(sorted(alphabet))


REDUCED_ALPHABET = _reduced_alphabet(Hashids)


def hashids_factory():
    salt = getattr(settings, 'URLBREVITY_SALT', '')
    if not salt:  # pragma: no cover
        logger.warning('Please use a salt, by setting `URLBREVITY_SALT`')
    return Hashids(salt=salt, min_length=1, alphabet=REDUCED_ALPHABET)


def encode(content_type, model_pk):
    encoder = hashids_factory()
    return encoder.encrypt(content_type, model_pk)


def decode(value):
    encoder = hashids_factory()
    return encoder.decrypt(value)


DecodedHashid = namedtuple('DecodedHashid', 'obj content_type hash decoded_hash')  # noqa


def get_encoded_object_or_404(hashid):
    try:
        decoded_tuple = decode(hashid)
    except:  # pragma: no cover
        msg = ("Unable to decode `{hashid!s}` into a useful "
               "tuple of (<ContentType.pk>, <Model.pk>)".format(hashid=hashid))
        logger.error(msg, exc_info=1, extra={'status': 404})
        raise Decode404(msg)

    if len(decoded_tuple) != 2:
        msg = ("Decoded tuple `{value!r}` does not consist of two "
               "values".format(value=decoded_tuple))
        logger.error(msg, extra={'status': 404})
        raise Decode404(msg)

    if not all(decoded_tuple):  # pragma: no cover
        msg = ("Decoded tuple `{value!r}` contains at least one useless "
               "value".format(value=decoded_tuple))
        logger.error(msg, extra={'status': 404})
        raise Decode404(msg)

    ct_pk, model_pk = decoded_tuple

    try:
        content_type = ContentType.objects.get_for_id(id=ct_pk)
    except ContentType.DoesNotExist:
        msg = ("Hashids decoded into a two-tuple OK, but "
               "<ContentType.pk={pk!s}> doesn't match anything in the cache "
               "or the database".format(pk=ct_pk))
        logger.error(msg, exc_info=1, extra={'status': 404})
        raise ContentType404(msg)

    try:
        obj = content_type.get_object_for_this_type(pk=model_pk)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        msg = ("Unable to find a model instance with a pk of {pk!s} using "
               "<ContentType.pk={ct_pk!s}>".format(pk=model_pk,
                                                   ct_pk=content_type.pk))
        logger.error(msg, exc_info=1, extra={'status': 404})
        raise Model404(msg)
    return DecodedHashid(obj=obj, content_type=content_type, hash=hashid,
                         decoded_hash=decoded_tuple)


EncodedModel = namedtuple('EncodedModel', 'obj content_type hash')


def encode_model_instance(obj):
    if not hasattr(obj, 'pk'):
        logger.info("Probably not a model instance")
        return None
    if not hasattr(obj, 'get_absolute_url'):
        logger.info("{obj!r} has no `get_absolute_url` method".format(obj=obj))
        return None
    try:
        content_type = ContentType.objects.get_for_model(obj)
    except (ContentType.DoesNotExist, DatabaseError):  # pragma: no cover
        # CT may not exist, or get_or_create may yield an IntegrityError etc.
        logger.info("Unable to resolve {value!r} into a ContentType instance",
                    exc_info=1)
        return None
    encoded = encode(content_type=content_type.pk, model_pk=obj.pk)
    return EncodedModel(obj=obj, content_type=content_type, hash=encoded)


def decode_model_instance(hashid):
    """
    Complement to encode_model_instance that returns None instead of
    raising an error.
    """
    try:
        return get_encoded_object_or_404(hashid).obj
    except Http404:   # pragma: no cover
        return None


def short_url(obj):
    encoded = encode_model_instance(obj=obj)
    if encoded is None:
        return None
    return reverse('urlbrevity:short', kwargs={'encoded_value': encoded.hash})


class ShortUrl(object):
    """
    Usage:
    class MyModel(Model):
        ...
        short_url = ShortUrl()
    """
    __slots__ = ()

    def __get__(self, instance, owner):
        return short_url(obj=instance)

    def __set__(self, instance, value):
        raise NotImplementedError("Can't re-bind, because there's no "
                                  "persistence backing this.")
