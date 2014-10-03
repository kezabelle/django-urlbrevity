# -*- coding: utf-8 -*-
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from pytest import mark
from urlbrevity.sitemaps import ShortUrlSitemap


@mark.django_db
def test_sitemaps():
    users = tuple(User.objects.create(username=x)
                  for x in range(0, 5))
    logs = tuple(LogEntry.objects.create(user=x, action_flag=ADDITION)
                 for x in users)

    class Sitemap(ShortUrlSitemap):
        models = (User, LogEntry)

    site = Site(domain='test.test')
    urls = Sitemap().get_urls(site=site)
    just_locs = tuple(x['location'] for x in urls)
    assert just_locs == (
        'http://test.test/redirect/yQfW',
        'http://test.test/redirect/9Rfo',
        'http://test.test/redirect/Rwf_',
        'http://test.test/redirect/YXf_',
        'http://test.test/redirect/oRf-',
        'http://test.test/redirect/9YuR',
        'http://test.test/redirect/y3uo',
        'http://test.test/redirect/4_uo',
        'http://test.test/redirect/rQuX',
        'http://test.test/redirect/_Yuw',
    )
