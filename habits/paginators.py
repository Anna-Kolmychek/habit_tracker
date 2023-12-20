from rest_framework.pagination import PageNumberPagination


class OwnHabitPaginator(PageNumberPagination):
    page_size = 5
