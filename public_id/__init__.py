# -*- coding: utf-8 -*-
import uuid

from django import forms
from django.db import models


CODE_LENGTH = 36


def gen_code():
    return str(uuid.uuid4())


class PublicIdFormField(forms.SlugField):
    def __init__(self, *args, **kwargs):
        kwargs['min_length'] = kwargs['max_length'] = CODE_LENGTH
        super(PublicIdFormField, self).__init__(*args, **kwargs)


class PublicIdDbField(models.SlugField):
    _max_length = CODE_LENGTH
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
