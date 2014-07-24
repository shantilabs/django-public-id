# -*- coding: utf-8 -*-
import uuid

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from public_id.utils import baseN


PUBLIC_ID_ALPHABET = getattr(settings, 'PUBLIC_ID_ALPHABET', (
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '_.-~'
))

max_base = len(PUBLIC_ID_ALPHABET)
real_max_length = len(baseN(2 ** 128, PUBLIC_ID_ALPHABET, max_base))
PUBLIC_ID_MAX_LENGTH = getattr(settings, 'PUBLIC_ID_MAX_LENGTH', real_max_length)

if PUBLIC_ID_MAX_LENGTH < real_max_length:
    raise ImproperlyConfigured('PUBLIC_ID_MAX_LENGTH must be great {}'.format(real_max_length))


def gen_code():
    return baseN(uuid.uuid4().int, PUBLIC_ID_ALPHABET, max_base)


class PublicIdFormField(forms.SlugField):
    def __init__(self, *args, **kwargs):
        kwargs['min_length'] = kwargs['max_length'] = PUBLIC_ID_MAX_LENGTH
        super(PublicIdFormField, self).__init__(*args, **kwargs)


class PublicIdDbField(models.SlugField):
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
        super(PublicIdDbField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['form_class'] = PublicIdFormField
        return super(PublicIdDbField, self).formfield(**kwargs)

    def pre_save(self, model_instance, add):
        if self.auto and not getattr(model_instance, self.attname):
            value = gen_code()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(PublicIdDbField, self).pre_save(model_instance, add)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.SlugField'
        args, kwargs = introspector(models.SlugField(*self._options[0], **self._options[1]))
        kwargs['max_length'] = self._max_length
        return field_class, args, kwargs
