import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

class AddBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('books:book_list')

class EditBookView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/edit_book.html'
    success_url = reverse_lazy('books:book_list')

    def get_object(self, queryset=None):
        # Obtiene el objeto Book basado en el ID de la URL
        return Book.objects.get(pk=self.kwargs['pk'])

def search_books_by_title(title):
    """
    Busca libros por título usando la API de OpenLibrary.
    
    Args:
        title (str): El título del libro a buscar.
    
    Returns:
        list: Una lista de libros que coinciden con el título.
    """
    url = "http://openlibrary.org/search.json"
    params = {'title': title}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        books = response.json().get('docs', [])
        return books
    else:
        print(f"Error: Unable to fetch data, received status code {response.status_code}")
        return []

def book_search_view(request):
    """
    Vista de Django para buscar libros por título.
    """
    title = request.GET.get('title', '')
    books = search_books_by_title(title)
    return JsonResponse(books, safe=False)
