import string
import uuid

import mock
from django.test import TestCase

from public_id import generate_id
from test_django.testapp.models import Post, PostNoAuto

TEST_UUID = uuid.UUID('249f19b0-7b54-4ad5-a0ba-92589079c0b8')
TEST_ID = '176qPOx1s18cmiQnX48BrW'
ALL_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase


class PublicIdFieldTestCase(TestCase):
    @mock.patch('uuid.uuid4', return_value=TEST_UUID)
    def test_generate_id(self, uuid_func):
        self.assertEqual(generate_id(), str(TEST_UUID))
        self.assertEqual(generate_id(ALL_CHARS), TEST_ID)

    @mock.patch('uuid.uuid4', return_value=TEST_UUID)
    def test_object(self, uuid_func):
        post = Post.objects.create()
        public_id = post.public_id
        self.assertEqual(public_id, TEST_ID)
        post.save()
        post.refresh_from_db()
        self.assertEqual(post.public_id, public_id)

    @mock.patch('uuid.uuid4', return_value=TEST_UUID)
    def test_object_non_auto(self, uuid_func):
        post = PostNoAuto.objects.create()
        self.assertFalse(post.public_id)
