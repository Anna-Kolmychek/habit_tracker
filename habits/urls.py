from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitPublicListAPIView, HabitOwnListAPIView, HabitRetrieveAPIView, \
    HabitUpdateAPIView, HabitDestroyAPIView

app_name = HabitsConfig.name


urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('public/', HabitPublicListAPIView.as_view(), name='habit_public_list'),
    path('own/', HabitOwnListAPIView.as_view(), name='habit_own_list'),
    path('detail/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('destroy/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_destroy'),
]
