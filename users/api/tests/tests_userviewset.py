import random

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.api.errors import FRIENDSHIP_WITH_YOURSELF_ERROR
from users.models import Friendship, User
from users.api.tests.utils import generate_random_friendships


class UserViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.users = [User.objects.create(username=f'user_{u}') for u in range(settings.REST_FRAMEWORK['PAGE_SIZE'])]
        generate_random_friendships(self.users)
        self.url = reverse('users:users-list')

    def test(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [{
            'id': u.id,
            'username': u.username,
            'friends': list(u.friends.values_list('id', flat=True)),
        } for u in self.users])


class UserViewSetRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')
        friendships = [
            Friendship.objects.create(
                initiator=self.user,
                partner=User.objects.create(username=f'user_{f}')
            ) for f in range(10)
        ]
        self.friends = list(map(lambda x: x.partner, friendships))
        # generate friendship between random friends
        friend_one, friend_two = random.sample(self.friends, 2)
        friend_one.friends.add(friend_two)

        self.url = reverse('users:users-detail', kwargs={'pk': self.user.pk})

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': self.user.id,
            'username': self.user.username,
            'friends': [{
                'id': f.id,
                'username': f.username,
                'friends': [{
                    'id': ff.id,
                    'username': ff.username
                } for ff in f.friends.all()]
            } for f in self.friends]
        })


class UserViewSetUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test_user')
        friendships = [
            Friendship.objects.create(
                initiator=self.user,
                partner=User.objects.create(username=f'user_{f}')
            ) for f in range(10)
        ]
        self.friends = list(map(lambda x: x.partner, friendships))
        # generate friendship between random friends
        friend_one, friend_two = random.sample(self.friends, 2)
        friend_one.friends.add(friend_two)

        self.url = reverse('users:users-detail', kwargs={'pk': self.user.pk})

    def test_put(self):
        new_friends = (random.choice(self.friends), User.objects.create(username='test_friend'))
        self.client.force_login(self.user)
        response = self.client.put(
            self.url,
            data={
                'id': self.user.id,
                'username': self.user.username,
                'friends_ids': [x.id for x in new_friends]
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': self.user.id,
            'username': self.user.username,
            'friends': [{
                'id': f.id,
                'username': f.username,
                'friends': [{
                    'id': ff.id,
                    'username': ff.username
                } for ff in f.friends.all()]
            } for f in new_friends]
        })

    def test_patch(self):
        new_friends = (random.choice(self.friends), User.objects.create(username='test_friend'))
        self.client.force_login(self.user)
        response = self.client.patch(
            self.url,
            data={
                'friends_ids': [x.id for x in new_friends]
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': self.user.id,
            'username': self.user.username,
            'friends': [{
                'id': f.id,
                'username': f.username,
                'friends': [{
                    'id': ff.id,
                    'username': ff.username
                } for ff in f.friends.all()]
            } for f in new_friends]
        })

    def test_foreign_user_update(self):
        foreign_user = random.choice(self.friends)
        self.client.force_login(foreign_user)
        response_patch = self.client.patch(
            path=self.url,
            data={
                'friends_ids': []
            }
        )
        response_put = self.client.put(
            path=self.url,
            data={
                'id': self.user.id,
                'username': self.user.username,
                'friends_ids': []
            }
        )
        self.assertEqual(response_patch.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_put.status_code, status.HTTP_403_FORBIDDEN)

    def test_friendship_with_yourself(self):
        self.client.force_login(self.user)
        response_patch = self.client.patch(
            path=self.url,
            data={
                'friends_ids': [self.user.id, ]
            }
        )
        response_put = self.client.put(
            path=self.url,
            data={
                'id': self.user.id,
                'username': self.user.username,
                'friends_ids': [self.user.id]
            }
        )
        self.assertEqual(response_patch.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_put.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_patch.data, {
            'friends_ids': [ErrorDetail(
                string='You cannot create friendship with yourself',
                code='unique'
            )]
        })
        self.assertEqual(response_put.data, {
            'friends_ids': [FRIENDSHIP_WITH_YOURSELF_ERROR, ]
        })
