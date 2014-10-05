# -*- coding: utf-8 -*-
from pytest import mark
import django
from django.contrib.auth.models import User
from django.template import Template
from django.template import Context
from .utils import encode_model_instance


@mark.django_db(transaction=True)
def test_converting_model_to_hashid():
    template = Template("""
    {% load urlbrevity %}
    <a href="/r/{{ obj|hashid }}/">test</a>
    """)
    user = User.objects.create()
    context = Context({
        'obj': user
    })
    rendered = template.render(context).strip()
    enc = encode_model_instance(user)
    expecting = '<a href="/r/{0}/">test</a>'.format(enc.hash)
    assert rendered == expecting


def test_converting_nothing_to_hashid():
    template = Template("""
    {% load urlbrevity %}
    <a href="/r/{{ wtf|hashid }}/">test2</a>
    """)
    context = Context()
    rendered = template.render(context).strip()
    assert rendered == '<a href="/r//">test2</a>'


def test_converting_dict_to_hashid():
    template = Template("""
    {% load urlbrevity %}
    <a href="/r/{{ obj|hashid }}/">test3</a>
    """)
    context = Context({
        'obj': {
            'test': 1,
        },
    })
    rendered = template.render(context).strip()
    assert rendered == '<a href="/r//">test3</a>'


@mark.django_db(transaction=True)
def test_generating_urls():
    template = Template("""
    {% load urlbrevity %}
    <a href="{% url 'urlbrevity:short' obj|hashid %}">test4</a>
    """)
    # special case the template for 1.4.x, where we need to the future url tag
    if django.VERSION[:2] == (1, 4):
        template = Template("""
        {% load urlbrevity %}
        {% load url from future %}
        <a href="{% url 'urlbrevity:short' obj|hashid %}">test4</a>
        """)
    user = User.objects.create()
    context = Context({
        'obj': user
    })
    rendered = template.render(context).strip()
    enc = encode_model_instance(user)
    expecting = '<a href="/redirect/{0}">test4</a>'.format(enc.hash)
    assert rendered == expecting


@mark.django_db(transaction=True)
def test_generating_short_urls_via_filter():
    template = Template("""
    {% load urlbrevity %}
    <a href="{{ obj|short_url }}">test5</a>
    """)
    user = User.objects.create()
    context = Context({
        'obj': user
    })
    rendered = template.render(context).strip()
    enc = encode_model_instance(user)
    expecting = '<a href="/redirect/{0}">test5</a>'.format(enc.hash)
    assert rendered == expecting
