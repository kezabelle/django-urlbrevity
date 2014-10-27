# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse, resolve, NoReverseMatch, Resolver404
from django.http import Http404
from ...utils import get_encoded_object_or_404, REDUCED_ALPHABET


class Command(BaseCommand):
    args = '<hashid hashid ...>'
    help = 'Discover what a short URL points to'

    def handle(self, *args, **options):
        for short_url in args:
            in_chars = set(short_url)
            all_chars = set(REDUCED_ALPHABET)
            leftovers = in_chars - all_chars
            if len(leftovers) > 0:
                msg = '`{surl!s}` contains invalid characters: {chars!s}'
                self.stdout.write(msg.format(surl=short_url,
                                             chars=', '.join(sorted(leftovers))))  # noqa
                continue  # to next iteration

            try:
                decoded = get_encoded_object_or_404(hashid=short_url)
            except Http404 as e:
                msg = '`{surl!s}` does not resolve to a model instance'
                self.stdout.write(msg.format(surl=short_url))
                continue  # to next iteration

            msg = "`{surl!s}` decodes into {ctmodel!r}"
            self.stdout.write(msg.format(surl=short_url,
                                         ctmodel=decoded.decoded_hash))

            msg = "`{surl!s}` resolves to a <{cls!s}> instance"
            self.stdout.write(msg.format(surl=short_url,
                                         cls=decoded.obj.__class__.__name__,
                                         pk=decoded.obj.pk))
            try:
                url = decoded.obj.get_absolute_url()
            except AttributeError:  # pragma: no cover
                msg = ("`{surl!s}` does not resolve to an object with a "
                       "`get_absolute_url` method")
                self.stdout.write(msg.format(surl=short_url))
            msg = '`{surl!s}` is a short URL for `{lurl!s}`'
            self.stdout.write(msg.format(surl=short_url, lurl=url))

            try:
                revurl = reverse('urlbrevity:short',
                                 kwargs={'encoded_value': short_url})
                func = resolve(revurl)
            except (NoReverseMatch, Resolver404) as e:  # pragma: no cover
                continue

            try:
                func_name = func.func.__name__
            except AttributeError:  # pragma: no cover ... python2
                func_name = func.func.func_name

            msg = ("`{surl!s}` is available via the `{view!s}` view, "
                   "via `{reverse!s}`")
            self.stdout.write(msg.format(surl=short_url, view=func_name,
                                         reverse=func.view_name))
