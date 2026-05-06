from rest_framework.pagination import CursorPagination


class DefaultCursorPagination(CursorPagination):
    page_size = 6
    ordering = 'created_at'
    page_size_query_param = 'page_size'
    max_page_size = 100