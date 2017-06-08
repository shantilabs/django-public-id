from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from .utils import base_n, generate_id

if settings.configured:
    assert not hasattr(settings, 'PUBLIC_ID_ALPHABET'), \
        'PUBLIC_ID_ALPHABET is not working anymore. Please use PUBLIC_ID_CHARS instead.'


def get_max_length(chars, default=36):
    real_max_length = default
    if chars:
        max_base = len(chars)
        real_max_length = len(base_n(2 ** 128, max_base, chars))

    max_length = getattr(settings, 'PUBLIC_ID_MAX_LENGTH', real_max_length)
    if max_length < real_max_length:
        raise ImproperlyConfigured('PUBLIC_ID_MAX_LENGTH must be great {}'.format(real_max_length))

    return max_length


class PublicIdFormField(forms.SlugField):
    pass


class PublicIdField(models.SlugField):
    def __init__(self, auto=False, *args, **kwargs):
        self.allowed_chars = getattr(settings, 'PUBLIC_ID_CHARS', None)
        kwargs['max_length'] = get_max_length(self.allowed_chars)

        self.auto = auto
        if auto:
            kwargs['editable'] = False
            kwargs['blank'] = True
            kwargs['unique'] = True

        super(PublicIdField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = PublicIdFormField
        return super(PublicIdField, self).formfield(**kwargs)

    def pre_save(self, model_instance, add):
        if self.auto and not getattr(model_instance, self.attname):
            value = generate_id(self.allowed_chars)
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(PublicIdField, self).pre_save(model_instance, add)
