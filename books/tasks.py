# books/tasks.py

from celery import shared_task
import requests
from books.models import Book
from celery.schedules import crontab
from celery import Celery

@shared_task
def fetch_books_from_openlibrary():
    """
    Obtiene los libros de OpenLibrary y guarda en la base de datos.
    """
    url = "http://openlibrary.org/search.json"
    params = {'title': 'some title'}  # Puedes ajustar los parámetros según sea necesario

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        books = response.json().get('docs', [])
        for book in books:
            cover_i = book.get('cover_i', '')
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg" if cover_i else ''
            
            publication_date = book.get('first_publish_year', '2000')
            publication_date = f"{publication_date}-01-01"  # Ajuste para formato YYYY-MM-DD
            
            pages = book.get('number_of_pages_median', 1)
            if not isinstance(pages, int):
                pages = 1
            
            Book.objects.update_or_create(
                title=book.get('title', ''),
                author=book.get('author_name', [''])[0] if book.get('author_name') else '',
                defaults={
                    'isbn': book.get('isbn', [''])[0] if book.get('isbn') else '',
                    'publication_date': publication_date,
                    'pages': pages,
                    'cover_image': cover_url
                }
            )
    else:
        print(f"Error: Unable to fetch data, received status code {response.status_code}")