from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTastCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='user1', password='123')
        self.user2 = User.objects.create(username='user2', password='123')

    def test_create_habit(self):
        """Тестирование создания привычки"""

        habit_action = 'test action'

        data = {
            'action': habit_action,
            'is_pleasant': True
        }

        self.client.force_authenticate(user=self.user1)

        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json()['action'],
            habit_action
        )

        self.assertTrue(
            Habit.objects.all().count() > 0
        )

    def test_public_list_habit(self):
        """Тестирование списка публичных привычек"""

        public_habit = Habit.objects.create(action='public', is_pleasant=True, is_public=True)
        private_habit = Habit.objects.create(action='private', is_pleasant=True)

        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            '/habits/public/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        response_habits_list = response.json()['results']

        self.assertEquals(
            len(response_habits_list),
            1
        )

        self.assertEquals(
            response_habits_list[0]['action'],
            'public'
        )

    def test_own_list_habit(self):
        """Тестирование списка привычек пользователя"""

        user1_habit = Habit.objects.create(action='user1', is_pleasant=True, owner=self.user1)
        user2_habit = Habit.objects.create(action='user2', is_pleasant=True, owner=self.user2)

        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            '/habits/own/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        response_habits_list = response.json()['results']

        self.assertEquals(
            len(response_habits_list),
            1
        )

        self.assertEquals(
            response_habits_list[0]['action'],
            'user1'
        )

    def test_retrive_habit(self):
        """Тестирование просмотра одной привычки"""

        habit = Habit.objects.create(action='test action', is_pleasant=True, owner=self.user1)

        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            f'/habits/detail/{habit.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json()['action'],
            'test action'
        )

    def test_update_habit(self):
        """Тестирование обновления привычки"""

        habit = Habit.objects.create(action='test action', is_pleasant=True, owner=self.user1)
        data = {'action': 'new action'}

        self.client.force_authenticate(user=self.user1)

        response = self.client.patch(
            f'/habits/update/{habit.pk}/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json()['action'],
            'new action'
        )

    def test_delete_habit(self):
        """Тестирование удаления привычки"""

        habit = Habit.objects.create(action='test action', is_pleasant=True, owner=self.user1)

        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(
            f'/habits/destroy/{habit.pk}/'
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEquals(
            len(Habit.objects.all()),
            0
        )
