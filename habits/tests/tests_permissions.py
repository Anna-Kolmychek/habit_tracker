from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTastCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='user1', password='123')
        self.user2 = User.objects.create(username='user2', password='123')

    def test_create_habit_permissions(self):
        """Тестирование доступа к созданию привычки"""

        data = {
            'action': 'test_action',
            'is_pleasant': True
        }

        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_public_list_habit_permissions(self):
        """Тестирование доступа к списку публичных привычек"""

        response = self.client.get(
            '/habits/public/'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            '/habits/public/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_own_list_habit_permissions(self):
        """Тестирование доступа к списку привычек пользователя"""

        response = self.client.get(
            '/habits/own/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            '/habits/own/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_retrive_habit_permissions(self):
        """Тестирование доступа к просмотру одной привычки"""

        habit = Habit.objects.create(action='test action', is_pleasant=True, owner=self.user1)

        response = self.client.get(
            f'/habits/detail/{habit.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(
            f'/habits/detail/{habit.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            f'/habits/detail/{habit.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_habit_permissions(self):
        """Тестирование доступа к обновлению привычки"""

        habit = Habit.objects.create(action='test action', is_pleasant=True, owner=self.user1)
        data = {'action': 'new action'}

        response = self.client.patch(
            f'/habits/update/{habit.pk}/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(
            f'/habits/update/{habit.pk}/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(
            f'/habits/update/{habit.pk}/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_habit_permissions(self):
        """Тестирование доступа к удалению привычки"""

        habit = Habit.objects.create(action='test action', is_pleasant=True, owner=self.user1)

        response = self.client.delete(
            f'/habits/destroy/{habit.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(
            f'/habits/destroy/{habit.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(
            f'/habits/destroy/{habit.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
