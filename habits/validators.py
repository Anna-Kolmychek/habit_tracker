from rest_framework.validators import ValidationError


class RelatedHabitVSRewardValidator:
    requires_context = True
    """
    Для обычной привычки исключает:
    одновременный выбор связанной привычки и указания вознаграждения;
    возможность отсутствия и связанной привычки и вознаграждения.
    """
    def __init__(self):
        pass

    def __call__(self, value, serializer_field):

        related_habit_value, reward_value, is_pleasant_value = None, None, None

        if serializer_field.instance:
            related_habit_value = serializer_field.instance.related_habit
            reward_value = serializer_field.instance.reward
            is_pleasant_value = serializer_field.instance.is_pleasant

        if 'related_habit' in dict(value).keys():
            related_habit_value = dict(value).get('related_habit')
        if 'reward' in dict(value).keys():
            reward_value = dict(value).get('reward')
        if 'is_pleasant' in dict(value).keys():
            is_pleasant_value = dict(value).get('is_pleasant')

        if related_habit_value and reward_value and not is_pleasant_value:
            raise ValidationError('Must be only one: related_habit or reward')

        if not (related_habit_value or reward_value) and not is_pleasant_value:
            raise ValidationError('Define something one: related_habit or reward')


class TimeDurationValidator:
    """Время выполнения должно быть не больше 120 секунд."""
    def __init__(self):
        pass

    def __call__(self, value):
        time_duration_value = dict(value).get('time_duration')

        if time_duration_value:
            if time_duration_value > 120:
                raise ValidationError('time_duration must less than 120')


class RelatedHabitValidator:
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""
    def __init__(self):
        pass

    def __call__(self, value):
        if dict(value).get('related_habit'):
            related_habit = dict(value).get('related_habit')
            if not related_habit.is_pleasant:
                raise ValidationError('related_habit must have is_pleasant=True')


class PleasantHabitValidator:
    requires_context = True
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    def __init__(self):
        pass

    def __call__(self, value, serializer_field):
        related_habit_value, reward_value = None, None

        if serializer_field.instance:
            related_habit_value = serializer_field.instance.related_habit
            reward_value = serializer_field.instance.reward

        if 'related_habit' in dict(value).keys():
            related_habit_value = dict(value).get('related_habit')
        if 'reward' in dict(value).keys():
            reward_value = dict(value).get('reward')

        if dict(value).get('is_pleasant'):
            if related_habit_value or reward_value:
                raise ValidationError('pleasant habit can`t have related_habit or reward')


class PeriodicalValidator:
    """
    Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
    Периодичность не может быть равна 0.
    """

    def __init__(self):
        pass

    def __call__(self, value):
        if not dict(value).get('periodical') is None:
            if dict(value).get('periodical') > 7 or dict(value).get('periodical') == 0:
                raise ValidationError('periodical must be no more than 7 and not equal 0')
