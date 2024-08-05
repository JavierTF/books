from django.urls import path
from .views import book_search_view
from .views import BookListView, AddBookView, EditBookView

app_name = 'books'

urlpatterns = [
    path('search/', book_search_view, name='book_search'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('add/', AddBookView.as_view(), name='add_book'),
    path('edit/<int:pk>/', EditBookView.as_view(), name='book_edit'),
]