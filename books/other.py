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
    Vista de Django para buscar libros por título y/o autor y guardar los libros en la base de datos.
    """
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    books = search_books(title=title, author=author)
    
    # Crear una lista de diccionarios con los datos deseados
    filtered_books = []
    for book in books:
        cover_i = book.get('cover_i', '')
        cover_url = f"https://covers.openlibrary.org/b/id/{cover_i}.jpg" if cover_i else ''

        # Convertir el año de publicación a formato de fecha
        first_publish_year = book.get('first_publish_year', '')
        publication_date = f"{first_publish_year}-01-01" if first_publish_year else '2000-01-01'

        # Obtener el número de páginas o establecer en 1 si está vacío o no presente
        number_of_pages_median = book.get('number_of_pages_median', '')
        pages = int(number_of_pages_median) if isinstance(number_of_pages_median, str) and number_of_pages_median.isdigit() else 1

        # Crear un diccionario con los datos del libro
        filtered_book = {
            'title': book.get('title', ''),
            'author_name': book.get('author_name', [''])[0] if book.get('author_name') else '',
            'isbn': book.get('isbn', [''])[0] if book.get('isbn') else '',
            'first_publish_year': first_publish_year,
            'number_of_pages_median': number_of_pages_median,
            'cover_url': cover_url
        }

        # Guardar el libro en la base de datos
        Book.objects.update_or_create(
            title=filtered_book['title'],
            author=filtered_book['author_name'],
            isbn=filtered_book['isbn'],
            cover_image=filtered_book['cover_url'],
            defaults={
                'publication_date': publication_date,
                'pages': pages,
            }
        )
        
        filtered_books.append(filtered_book)

        return redirect('books:book_list')
    
    # return JsonResponse(filtered_books, safe=False)