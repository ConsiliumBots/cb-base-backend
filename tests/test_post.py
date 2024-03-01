from app.factories import UserFactory, PostFactory
from app.models import Post
from rest_framework.test import APIClient
from django.test import TestCase
import json
from rest_framework_simplejwt.tokens import RefreshToken


def login(user):
    """
    Given a user, it returns authorization token.
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh)


class PostTestCase(TestCase):

    def setUp(self):
        """
        set up test. Create models and associations.
        """

        # create two users
        self.user_A = UserFactory(username="user_A")
        self.user_B = UserFactory(username="user_B")

        # get user tokens
        self.user_A_token = login(self.user_A)
        self.user_B_token = login(self.user_B)

        # create two posts per user
        self.posts = {
            self.user_A: [PostFactory(user=self.user_A) for _ in range(2)],
            self.user_B: [PostFactory(user=self.user_B) for _ in range(2)]

        }

        # create client
        self.client = APIClient()

    def test_unauthorized_retrieve(self):
        """
        Test unauthorized retrieve.
        Only unauthenticated users can't retrieve posts.
        """

        # get any post
        post_A = self.posts[self.user_A][0]

        # test unauthenticated (no credentials)
        self.client.credentials()
        response = self.client.get(f"/post/{post_A.pk}/")
        self.assertEqual(response.status_code, 403)

    def test_authorized_retrieve(self):
        """
        Test authorized retrieve.
        Users should be able to access any post.
        """

        # get post A
        post_A = self.posts[self.user_A][0]

        # get post B
        post_B = self.posts[self.user_B][0]

        # authenticate client with user A
        self.client.credentials(HTTP_AUTHORIZATION=self.user_A_token)

        # access post A
        response = self.client.get(f"/post/{post_A.pk}/")
        self.assertEqual(response.status_code, 200)

        # access post B
        response = self.client.get(f"/post/{post_B.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_list(self):
        """
        Test unauthorized list.
        Only unauthorized users can't list.
        """

        # test unauthenticated (no credentials)
        self.client.credentials()

        # get posts
        response = self.client.get("/post/")

        # assert
        self.assertEqual(response.status_code, 403)

    def test_authorized_list(self):
        """Test authorized list."""

        # set token
        self.client.credentials(HTTP_AUTHORIZATION=self.user_A_token)

        # get objects. check count
        response = self.client.get(f"/post/")
        self.assertEqual(response.status_code, 200)
        self.asserEqual(len(response.data), 4)

    def test_unauthorized_post(self):
        """Test unauthorized post."""

        # generate payload
        payload = {'content': 'content'}

        # test unauthenticated (no credentials)
        self.client.credentials()

        # get response
        response = self.client.post(
            "/post/",
            data=json.dumps(payload),
            content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_authorized_post(self):
        """Test authorized post"""

        # generate payload
        payload = {'content': 'content'}

        # authenticate
        self.client.credentials(HTTP_AUTHORIZATION=self.user_A_token)

        # get response
        response = self.client.post(
            f"/post/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_patch(self):
        """
        Test unauthorized patch.
        Two cases:
        - unauthenticated
        - not owner of post
        """

        # generate payload and get post
        payload = {'content': 'content'}
        post_A = self.posts[self.user_A][0]

        # first: unauthenticated trying to patch post A
        self.client.credentials()
        response = self.client.patch(
            f"/post/{post_A.pk}/",
            data=json.dumps(payload),
            content_type="application/json")
        self.assertEqual(response.status_code, 403)

        # second: user B trying to patch post A
        self.client.credentials(HTTP_AUTHORIZATION=self.user_B_token)
        response = self.client.patch(
            f"/post/{post_A.pk}/",
            data=json.dumps(payload),
            content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_authorized_patch(self):
        """Test authorized patch."""

        # generate payload and get post
        payload = {'content': 'content'}
        post_A = self.posts[self.user_A][0]
        self.client.credentials(HTTP_AUTHORIZATION=self.user_A_token)

        # patch
        response = self.client.patch(
            f"/post/{post_A.pk}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_delete(self):
        """
        Test unauthorized delete.
        Unauthenticated users and non-owners can't delete.
        """

        # get post
        post_A = self.posts[self.user_A][0]

        # unauthenticated
        self.client.credentials()
        response = self.client.delete(f"/post/{post_A.pk}/")
        self.assertEqual(response.status_code, 403)

        # non-owner
        self.client.credentials(HTTP_AUTHORIZATION=self.user_B_token)
        response = self.client.delete(f"/post/{post_A.pk}/")
        self.assertEqual(response.status_code, 403)

    def test_authorized_delete(self):
        """Test authorized delete"""

        # get post
        post_A = self.posts[self.user_A][1]

        # authenticate
        self.client.credentials(HTTP_AUTHORIZATION=self.user_A_token)

        # delete
        response = self.client.delete(f"/post/{post_A.pk}/")
        self.assertEqual(response.status_code, 204)
