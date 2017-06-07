import uuid

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from public_id.utils import base_n

VERSION = (2, 1, 0)
__version__ = '.'.join(map(str, VERSION))

assert not hasattr(settings, 'PUBLIC_ID_ALPHABET'), \
    'PUBLIC_ID_ALPHABET is not working anymore. Please use PUBLIC_ID_CHARS instead.'

PUBLIC_ID_CHARS = getattr(settings, 'PUBLIC_ID_CHARS', None)

if PUBLIC_ID_CHARS:
    max_base = len(PUBLIC_ID_CHARS)
    real_max_length = len(base_n(2 ** 128, max_base, numerals=PUBLIC_ID_CHARS))
else:
    real_max_length = 36

PUBLIC_ID_MAX_LENGTH = getattr(settings, 'PUBLIC_ID_MAX_LENGTH', real_max_length)

if PUBLIC_ID_MAX_LENGTH < real_max_length:
    raise ImproperlyConfigured('PUBLIC_ID_MAX_LENGTH must be great {}'.format(real_max_length))


def generate_id():
    if PUBLIC_ID_CHARS:
        return base_n(uuid.uuid4().int, max_base, numerals=PUBLIC_ID_CHARS)
    else:
        return str(uuid.uuid4())


class PublicIdFormField(forms.SlugField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = PUBLIC_ID_MAX_LENGTH
        super(PublicIdFormField, self).__init__(*args, **kwargs)


class PublicIdField(models.SlugField):
    _max_length = PUBLIC_ID_MAX_LENGTH
    _options = None

    def __init__(self, auto=False, *args, **kwargs):
        self.auto = auto
        if auto:
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True
        kwargs['max_length'] = self._max_length
        self._options = (args, kwargs)
        super(PublicIdField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = PublicIdFormField
        return super(PublicIdField, self).formfield(**kwargs)

    def pre_save(self, model_instance, add):
        if self.auto and not getattr(model_instance, self.attname):
            value = generate_id()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(PublicIdField, self).pre_save(model_instance, add)
