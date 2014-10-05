# -*- coding: utf-8 -*-
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from pytest import mark
from django.utils.encoding import force_text
from .utils import encode_model_instance
from .sitemaps import ShortUrlSitemap


@mark.django_db(transaction=True)
def test_sitemaps():
    users = tuple(User.objects.create(username=force_text(x))
                  for x in range(0, 5))
    logs = tuple(LogEntry.objects.create(user=x, action_flag=ADDITION)
                 for x in users)

    class Sitemap(ShortUrlSitemap):
        models = (User, LogEntry)

    site = Site(domain='test.test')
    urls = Sitemap().get_urls(site=site)
    just_locs = sorted(x['location'] for x in urls)
    # manually re-construct them
    constructed = sorted(
        'http://test.test/redirect/{0}'.format(encode_model_instance(x).hash)
        for x in set(users + logs)
    )
    assert just_locs == constructed
