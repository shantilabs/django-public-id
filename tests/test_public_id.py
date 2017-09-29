import random
import string
import sys
import uuid

import mock
import pytest
from django.db import IntegrityError
from django.db import models

from django_test_project.testapp.models import Post, PostNoAuto
from public_id import generate_id, PublicIdField
from public_id.fields import get_minimal_length

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
    assert generate_id() == TEST_SEQUENCE[0:22]

    assert generate_id('01', 36) == TEST_BINARY_SEQUENCE
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
    Post.objects.create()

    with pytest.raises(IntegrityError):
        Post.objects.create()


@pytest.mark.django_db
def test_object_non_auto():
    post = PostNoAuto.objects.create()
    assert post.public_id == ''


@pytest.mark.django_db
@pytest.mark.parametrize('length', [25, 35])
def test_length(length, systemrandom_patch, settings):
    settings.PUBLIC_ID_MAX_LENGTH = length

    class TestModel1(models.Model):
        public_id = PublicIdField(auto=True)

        class Meta:
            app_label = 'testapp'
            db_table = 'testapp_tablewithidonly'

    record = TestModel1.objects.create()

    assert len(record.public_id) == length
    assert record.public_id == TEST_SEQUENCE[0:length]


@pytest.mark.django_db
def test_uuid(uuid_patch, settings):
    settings.PUBLIC_ID_CHARS = None

    class TestModel2(models.Model):
        public_id = PublicIdField(auto=True)

        class Meta:
            app_label = 'testapp'
            db_table = 'testapp_tablewithidonly'


    record = TestModel2.objects.create()

    assert record.public_id == str(TEST_UUID)


@pytest.mark.django_db
def test_legacy_public_id_alphabet(systemrandom_patch, settings):
    delattr(settings, 'PUBLIC_ID_CHARS')
    settings.PUBLIC_ID_ALPHABET = '01'

    class TestModel3(models.Model):
        public_id = PublicIdField(auto=True)

        class Meta:
            app_label = 'testapp'
            db_table = 'testapp_tablewithidonly'

    record = TestModel3.objects.create()

    assert record.public_id[0:len(TEST_BINARY_SEQUENCE)] == TEST_BINARY_SEQUENCE


def test_check_length():
    assert get_minimal_length('01') == 128
    assert get_minimal_length('0123') == 64
    assert get_minimal_length(ALL_CHARS) == 22
