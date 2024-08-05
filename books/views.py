import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm

def search_books(title='', author=''):
    """
    Busca libros por título y/o autor usando la API de OpenLibrary.
    
    Args:
        title (str): El título del libro a buscar.
        author (str): El autor del libro a buscar.
    
    Returns:
        list: Una lista de libros que coinciden con los criterios de búsqueda.
    """
    url = "http://openlibrary.org/search.json"
    params = {}
    
    if title:
        params['title'] = title
    if author:
        params['author'] = author
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        books = response.json().get('docs', [])
        return books
    else:
        print(f"Error: Unable to fetch data, received status code {response.status_code}")
        return []

def book_search_view(request):
    """
    Vista de Django para buscar libros por título y/o autor.
    """
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    books = search_books(title=title, author=author)
    return JsonResponse(books, safe=False)

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        title_query = self.request.GET.get('title')
        author_query = self.request.GET.get('author')

        if title_query:
            queryset = queryset.filter(title__icontains=title_query)
        if author_query:
            queryset = queryset.filter(author__icontains=author_query)
            
        return queryset

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
    
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_object(self, queryset=None):
        # Obtiene el objeto Book basado en el ID de la URL
        return Book.objects.get(pk=self.kwargs['pk'])
    
class DeleteBookView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:book_list')