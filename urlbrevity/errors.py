# -*- coding: utf-8 -*-
from django.http import Http404


class Decode404(Http404): pass
class ContentType404(Http404): pass
class Model404(Http404): pass
