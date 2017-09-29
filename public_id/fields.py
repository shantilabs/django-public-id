import uuid

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models

from .utils import generate_sequence


def get_allowed_chars():
    return getattr(settings, 'PUBLIC_ID_CHARS',
                   getattr(settings, 'PUBLIC_ID_ALPHABET', None))  # legacy name


def get_length():
    return getattr(settings, 'PUBLIC_ID_LENGTH',
                   getattr(settings, 'PUBLIC_ID_MAX_LENGTH', None))  # legacy name


def get_minimal_length(chars):
    """
    Return the length of string that can store 128 bits of information
    """
    alphabet_length = len(set(chars))
    assert alphabet_length >= 2

    variants_threshold = 2**128
    variants = 1

    result = 0

    while variants < variants_threshold:
        variants *= alphabet_length
        result += 1

    return result


def check_length(length, chars):
    """
    Check if ID with given length and alphabet can store at least 128 bits
    """

    min_length = get_minimal_length(chars)

    if length < min_length:
        raise ImproperlyConfigured('PUBLIC_ID_LENGTH must at least {}'.format(min_length))


def generate_id(chars=None, length=None):
    if not chars:
        chars = get_allowed_chars()

    if not length:
        length = get_length() or get_minimal_length(chars)

    if chars:
        return generate_sequence(chars, length)
    else:
        return str(uuid.uuid4())


class PublicIdFormField(forms.SlugField):
    pass


class PublicIdField(models.SlugField):

    def __init__(self, auto=False, *args, **kwargs):
        self.allowed_chars = get_allowed_chars()

        if self.allowed_chars:
            length = get_length()
            if length:
                check_length(length, self.allowed_chars)
            else:
                length = get_minimal_length(self.allowed_chars)

            kwargs['max_length'] = length
        else:
            kwargs['max_length'] = 36  # length of UUID

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
            value = generate_id(self.allowed_chars, self.max_length)
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(PublicIdField, self).pre_save(model_instance, add)
