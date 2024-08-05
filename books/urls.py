from django.urls import path
from .views import BookListView, AddBookView, EditBookView, BookDetailView, DeleteBookView, BookListViewDRF
from .views import BookDetailView

app_name = 'books'

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('add/', AddBookView.as_view(), name='add_book'),
    path('edit/<int:pk>/', EditBookView.as_view(), name='book_edit'),
    path('detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('delete/<int:pk>/delete/', DeleteBookView.as_view(), name='book_delete'),
    path('books-list/', BookListViewDRF.as_view(), name='book-list'),
    path('book-detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]