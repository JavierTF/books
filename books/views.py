import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

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
