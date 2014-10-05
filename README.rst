===========
URL Brevity
===========

Another short-URL generator, based on `Hashids`_ and a reduced alphabet.

.. image:: https://travis-ci.org/kezabelle/django-urlbrevity.svg?branch=master
    :target: https://travis-ci.org/kezabelle/django-urlbrevity


Why a reduced alphabet?
-----------------------

Because if you're going to bother with a short URL, it needs to be readable
and easily audible, without constantly double-checking you've not misread or
misheard.

Why `Hashids`_
--------------

Because assuming your model primary keys are integers, it's a dirt simple way
of encoding a tuple in a reasonably small space. One could also just use
``django.utils.http.int_to_base36`` of course.

Usage
-----

in your settings module::

    INSTALLED_APPS = (
        # ...
        'urlbrevity',
        # ...
    )

in your root urlconf::

    from django.conf.urls import patterns, url, include
    import urlbrevity

    urlpatterns = patterns("",
        # ...
        url(r'redirect/', include(urlbrevity.redirects)),
        # Or if you don't want to redirect ...
        url(r'no_redirect/', include(urlbrevity.no_redirects)),
        # ...
    )

.. note:: You obviously don't have to use `redirect` and `no_redirect` as the
          url prefixes, and you should only use one or the other, really.

in your templates::

    {% load urlbrevity %}
    <a href="{% url 'urlbrevity:short' my_model_instance|hashid %}">...</a>
    or ...
    <a href="{{ my_model_instance|short_url }}">

in your python::

    import urlbrevity
    obj = MyModel.objects.get(pk='...')
    encoded = urlbrevity.encode_model_instance(obj=obj)
    value = encoded.hash
    url = reverse('urlbrevity:short', kwargs={'encoded_value': value})
    # or ...
    url2 = urlbrevity.short_url(obj)

    # to re-inflate ...
    obj_again = urlbrevity.decode_model_instance(value)



Why internal redirects?
-----------------------

Because mobile is an important space, and even on 3G+ connections, redirects
are another round-trip that may fail or be slow. Easier to just render the
intended output if possible.

.. note:: You can use 301 (permanent) redirects if you prefer, by including
          ``urlbrevity.redirects`` instead of ``urlbrevity.no_redirects``, you
          can also stitch together your own stuff based on the existing
          views and named URLconfs.


.. _Hashids: http://hashids.org/python/
