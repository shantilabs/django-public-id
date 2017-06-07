from django.test import TestCase
import mock
import uuid


from test_django.testapp.models import Post
from public_id import generate_id

TEST_UUID = uuid.uuid4()


class TestPublicIdField(TestCase):

    def test_logic(self):
        post = Post.objects.create()
        self.assertTrue(post.public_id)

        public_id = post.public_id
        post.save()
        post.refresh_from_db()
        self.assertEqual(public_id, post.public_id)

    @mock.patch('uuid.uuid4', return_value=TEST_UUID)
    def test_value(self, uuid_func):
        self.assertEqual(uuid.uuid4(), TEST_UUID)

        new_id = generate_id()
        self.assertTrue(new_id)
        self.assertEqual(new_id, generate_id())

        post = Post.objects.create()
        self.assertEqual(post.public_id, new_id)
