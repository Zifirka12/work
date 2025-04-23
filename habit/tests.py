from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email="test@example.com")

        self.test_habit = Habit.objects.create(
            habit_owner=self.test_user,
            habit_place="At home",
            habit_time="2025-04-07T18:30:00+03:00",
            habit_action="Do breathing exercises",
            is_habit_pleasantly=True,
            habit_periodicity=1,
            reward="Fresh air in lungs!",
            habit_time_to_complete="00:03:00",
        )

        # Авторизуем клиента
        self.client.force_authenticate(user=self.test_user)

    def test_create_habit(self):
        self.assertEqual(Habit.objects.count(), 1)

    def test_retrieve_habit(self):
        url = reverse("habit:retrieve_habits", args=(self.test_habit.pk,))
        response = self.client.get(url)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("habit_periodicity"), self.test_habit.habit_periodicity)

    def test_list_habits(self):
        url = reverse("habit:habit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        url = reverse("habit:update_habits", args=(self.test_habit.pk,))
        update_data = {
            "habit_place": "In the kitchen",
            "habit_time": "2025-04-07T18:30:00+03:00",
            "habit_action": "Take pills",
            "is_habit_pleasantly": False,
            "habit_periodicity": 1,
            "habit_time_to_complete": "00:02:00",
        }
        response = self.client.patch(url, update_data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get("habit_place"), "In the kitchen")

    def test_delete_habit(self):
        url = reverse("habit:delete_habits", args=(self.test_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_public_habit_list(self):
        url = reverse("habit:public_habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
