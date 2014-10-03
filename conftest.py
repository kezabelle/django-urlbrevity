# -*- coding: utf-8 -*-
def pytest_configure():
    import django
    from django.conf import settings
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'urlbrevity',
        ),
        MIDDLEWARE_CLASSES=(),
        URLBREVITY_SALT='hello i am a test',
        ROOT_URLCONF='urlbrevity.test_urlconf',
    )
    if hasattr(django, 'setup'):
        django.setup()
