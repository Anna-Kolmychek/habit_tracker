import json

from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTastCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='user1', password='123')
        self.user2 = User.objects.create(username='user2', password='123')

    def test_related_habit_vs_reward_validator(self):
        """Тестирование наличия связанной привычки & вознаграждение"""

        habit_pleasant = Habit.objects.create(action='pleasant action', is_pleasant=True)
        self.client.force_authenticate(user=self.user1)

        # Case 1. Создаем привычку. Одновременно добавляем и связанную привычку и вознаграждение
        data = {
            'action': 'test action',
            'related_habit': habit_pleasant.pk,
            'reward': 'some reward'
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 2. Создаем привычку. Нет ни связанной привычки, ни вознаграждения
        data = {
            'action': 'test action',
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 3. Обновляем привычку: была связанная привычка, добавляем вознаграждения
        habit1 = Habit.objects.create(action='test action', related_habit=habit_pleasant, owner=self.user1)
        data = {
            'reward': 'test',
        }
        response = self.client.patch(
            f'/habits/update/{habit1.pk}/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 4. Обновляем привычку: было вознаграждение, добавляем связанную привычку
        habit2 = Habit.objects.create(action='test action', reward='test', owner=self.user1)
        data = {
            'related_habit': habit_pleasant.pk
        }
        response = self.client.patch(
            f'/habits/update/{habit2.pk}/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 5. Обновляем привычку: замена с обнулением вознаграждения
        habit3 = Habit.objects.create(action='test action', reward='test', owner=self.user1)
        data = {
            'reward': None,
            'related_habit': habit_pleasant.pk
        }
        response = self.client.patch(
            f'/habits/update/{habit3.pk}/',
            data=data,
            format='json'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # Case 6. Обновляем привычку: замена с обнулением связанной привычки
        habit4 = Habit.objects.create(action='test action', related_habit=habit_pleasant, owner=self.user1)
        data = {
            'related_habit': None,
            'reward': 'test'
        }
        response = self.client.patch(
            f'/habits/update/{habit4.pk}/',
            data=data,
            format='json'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_time_duration_validator(self):
        """Проверяем время выполнения (должно быть не больше 120)"""

        self.client.force_authenticate(user=self.user1)

        # Case 1. Создаем привычку, время выполнения больше 120
        data = {
            'action': 'test action',
            'reward': 'test reward',
            'time_duration': 121
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 2. Создаем привычку, время выполнения не больше 120
        data = {
            'action': 'test action',
            'reward': 'test reward',
            'time_duration': 120
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Case 3. Обновляем привычку, время выполнения больше 120
        habit_id = response.json()['id']
        data = {
            'time_duration': 121
        }
        response = self.client.patch(
            f'/habits/update/{habit_id}/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_related_habit_validator(self):
        """Проверяем, что в связанные привычки могут попадать только привычки с признаком приятной привычки."""

        pleasant_habit = Habit.objects.create(action='test', is_pleasant=True, owner=self.user1)
        other_habit = Habit.objects.create(action='test', reward='test', owner=self.user1)
        self.client.force_authenticate(user=self.user1)

        # Case 1. Создаем привычку, в связанных не из приятных
        data = {
            'action': 'test action',
            'related_habit': other_habit.pk
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 2. Создаем привычку, в связанных приятная
        data = {
            'action': 'test action',
            'related_habit': pleasant_habit.pk
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Case 3. Обновляем привычку, в связанных не из приятных
        habit_id = response.json()['id']
        data = {
            'related_habit': other_habit.pk
        }
        response = self.client.patch(
            f'/habits/update/{habit_id}/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_pleasant_habit_validator(self):
        """Проверяем, что у риятной привычки не может быть вознаграждения или связанной привычки."""

        habit = Habit.objects.create(action='test', reward='test', owner=self.user1)
        self.client.force_authenticate(user=self.user1)

        # Case 1. Создаем приятную привычку, есть связанная привычка
        data = {
            'action': 'test action',
            'is_pleasant': True,
            'related_habit': habit.pk
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 2. Создаем приятную привычку, есть вознаграждение
        data = {
            'action': 'test action',
            'is_pleasant': True,
            'reward': 'test'
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 3. Создаем приятную привычку без связанной и вознаграждения
        data = {
            'action': 'test action',
            'is_pleasant': True
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Case 4. Обновляем обычную привычку на приятную без удаления связанной
        pleasant_habit = Habit.objects.get(pk=response.json()['id'])
        habit1 = Habit.objects.create(action='test', related_habit=pleasant_habit, owner=self.user1)
        data = {
            'is_pleasant': True,
        }
        response = self.client.patch(
            f'/habits/update/{habit1.pk}/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 5. Обновляем обычную привычку на приятную c удалением связанной
        data = {
            'is_pleasant': True,
            'related_habit': None
        }
        response = self.client.patch(
            f'/habits/update/{habit1.pk}/',
            data=data,
            format='json'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # Case 5. Обновляем обычную привычку на приятную без удаления вознаграждения
        habit2 = Habit.objects.create(action='test', reward='test', owner=self.user1)
        data = {
            'is_pleasant': True,
        }
        response = self.client.patch(
            f'/habits/update/{habit2.pk}/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 6. Обновляем обычную привычку на приятную c удалением вознаграждения
        data = {
            'is_pleasant': True,
            'reward': None
        }
        response = self.client.patch(
            f'/habits/update/{habit2.pk}/',
            data=data,
            format='json'
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_periodical_validator(self):
        """Проверяем периодичность не больше 7 и не равно 0"""

        self.client.force_authenticate(user=self.user1)

        # Case 1. Создаем привычку, периодичность больше 7
        data = {
            'action': 'test action',
            'reward': 'test reward',
            'periodical': 8
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 2. Создаем привычку, периодичность 0
        data = {
            'action': 'test action',
            'reward': 'test reward',
            'periodical': 0
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 3. Создаем привычку, периодичность от 0 до 7
        data = {
            'action': 'test action',
            'reward': 'test reward',
            'periodical': 7
        }
        response = self.client.post(
            '/habits/create/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Case 4. Обновляем привычку, периодичность больше 7
        habit_id = response.json()['id']
        data = {
            'periodical': 8
        }
        response = self.client.patch(
            f'/habits/update/{habit_id}/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Case 5. Обновляем привычку, периодичность 0
        data = {
            'periodical': 0
        }
        response = self.client.patch(
            f'/habits/update/{habit_id}/',
            data=data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
