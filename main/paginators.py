from rest_framework.pagination import PageNumberPagination


class LessonsPaginator(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'per_page'
    max_page_size = 200
