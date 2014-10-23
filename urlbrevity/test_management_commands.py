# -*- coding: utf-8 -*-
from pytest import mark
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
try:
    from django.utils.six import StringIO
except ImportError:
    from StringIO import StringIO
from .utils import encode


@mark.django_db(transaction=True)
def test_urlbrevity_management_command():
    ct = ContentType.objects.get_for_model(User)
    user = User.objects.create(username='test_urlbrevity_management_command1')
    user2 = User.objects.create(username='test_urlbrevity_management_command2')
    tup1 = (ct.pk, user.pk)
    tup2 = (ct.pk, user2.pk)
    enc = encode(*tup1)
    enc2 = encode(*tup2)
    stdout = StringIO()
    call_command('urlbrevity', '1lLi', 'yyyy', enc, enc2, verbosity=2,
                 interactive=False, stdout=stdout)
    msg = ("`1lLi` contains invalid characters: 1, l, L\n"
           "`yyyy` does not resolve to a model instance\n"
           "`{enc}` decodes into {tup1!r}\n"
           "`{enc}` resolves to a <User> instance\n"
           "`{enc}` is a short URL for `/test_user/{pk1}/`\n"
           "`{enc}` is available via the `do_redirect` view\n"
           "`{enc2}` decodes into {tup2!r}\n"
           "`{enc2}` resolves to a <User> instance\n"
           "`{enc2}` is a short URL for `/test_user/{pk2}/`\n"
           "`{enc2}` is available via the `do_redirect` view\n")
    assert stdout.getvalue() == msg.format(enc=enc, enc2=enc2, tup1=tup1,
                                           tup2=tup2, pk1=user.pk,
                                           pk2=user2.pk)
