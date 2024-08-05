from django.urls import path
from .views import book_search_view, book_list

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('search/', book_search_view, name='book_search'),
]