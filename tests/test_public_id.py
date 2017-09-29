import sys
import string
import uuid
import random

import pytest
import mock
from django.test import TestCase
from django.db import IntegrityError

from public_id import generate_id, base_n
from test_django.testapp.models import Post, PostNoAuto

TEST_UUID = uuid.UUID('249f19b0-7b54-4ad5-a0ba-92589079c0b8')
ALL_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase

# Sequence that we got with random seed=0 and chars=ALL_CHARS
if sys.version_info.major == 2:
    TEST_SEQUENCE = 'QKqgvpMitAUvhKCfUYOTjJTGt6qBUXtRgNy0'
    TEST_BINARY_SEQUENCE = '110010100111011011110111000111010110' 
else:
    TEST_SEQUENCE = 'SoMUq2gZwvpWORjZumBVWdw8i8M6DPgWyJPC'
    TEST_BINARY_SEQUENCE = '110111111001001010011011101110001011' 

@pytest.yield_fixture
def systemrandom_patch():
    with mock.patch('random.SystemRandom', side_effect=lambda: random.Random(0)):
        yield


@pytest.yield_fixture
def uuid_patch():
    with mock.patch('uuid.uuid4', return_value=TEST_UUID):
        yield


def test_generate_id(systemrandom_patch):
    assert generate_id('01') == TEST_BINARY_SEQUENCE
    assert generate_id(ALL_CHARS, 36) == TEST_SEQUENCE
    assert len(generate_id('a', 99)) == 99


@pytest.mark.django_db
def test_save_and_reload_model(systemrandom_patch):
    post = Post.objects.create()
    public_id = post.public_id
    assert public_id == TEST_SEQUENCE[0:22]

    post.save()
    post.refresh_from_db()

    assert post.public_id == public_id


@pytest.mark.django_db
def test_unique_constraint(systemrandom_patch):
    post = Post.objects.create()

    with pytest.raises(IntegrityError):
        post = Post.objects.create()


@pytest.mark.django_db
def test_object_non_auto():
    post = PostNoAuto.objects.create()
    assert post.public_id == ''


@pytest.mark.django_db
@pytest.mark.parametrize('length', [25, 35])
def test_length(length, systemrandom_patch, settings):
    settings.PUBLIC_ID_MAX_LENGTH = length

    post = Post.objects.create()

    assert len(post.public_id) == length
    assert post.public_id == TEST_SEQUENCE[0:length]


@pytest.mark.django_db
def test_uuid(uuid_patch, settings):
    settings.PUBLIC_ID_CHARS = None

    post = Post.objects.create()

    assert post.public_id == str(TEST_UUID)
