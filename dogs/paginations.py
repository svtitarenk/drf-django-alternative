from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 5
    # параметр по которому можно в headers передавать настройки page_size
    page_size_query_param = 'page_size'
    max_page_size = 10
