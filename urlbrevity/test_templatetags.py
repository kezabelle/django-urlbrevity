# -*- coding: utf-8 -*-
from pytest import mark
from django.contrib.auth.models import User
from django.template import Template
from django.template import Context


@mark.django_db
def test_converting_model_to_hashid():
    template = Template("""
    {% load urlbrevity %}
    <a href="/r/{{ obj|hashid }}/">test</a>
    """)
    context = Context({
        'obj': User.objects.create()
    })
    rendered = template.render(context).strip()
    assert rendered == '<a href="/r/yQfW/">test</a>'


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


@mark.django_db
def test_generating_urls():
    template = Template("""
    {% load urlbrevity %}
    <a href="{% url 'urlbrevity:short' obj|hashid %}">test4</a>
    """)
    context = Context({
        'obj': User.objects.create()
    })
    rendered = template.render(context).strip()
    assert rendered == '<a href="/redirect/yQfW">test4</a>'

@mark.django_db
def test_generating_short_urls_via_filter():
    template = Template("""
    {% load urlbrevity %}
    <a href="{{ obj|short_url }}">test5</a>
    """)
    context = Context({
        'obj': User.objects.create()
    })
    rendered = template.render(context).strip()
    assert rendered == '<a href="/redirect/yQfW">test5</a>'
