===========
URL Brevity
===========

Another short-URL generator, based on `Hashids`_ and a reduced alphabet.


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

.. _Hashids: http://hashids.org/python/
