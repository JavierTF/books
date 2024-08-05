# OpenLibrary

## Descripción

Este es un proyecto Django que utiliza Celery y Redis para gestionar tareas asíncronas. En este proyecto, se obtiene y guarda información de libros desde OpenLibrary.

## Requisitos

- Python 3.9.6
- Django 4.2
- Celery 5.2.7 (compatible con Django 4.2)
- Redis
- psycopg2-binary
- Otros requisitos (listados en `requirements.txt`)

## Instalación

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/JavierTF/books.git
   cd openlibrary

2. **Crea un entorno virtual e instálalo**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

3. **Instala dependencias**
    ```bash
    pip install -r requirements.txt

4. **Configura Redis**
    ```bash
    redis-server

5. **Crea la base de datos y realiza las migraciones**
    # BD books, USER postgres, PASW postgres 
    ```bash
    python manage.py makemigrations
    python manage.py migrate

6. **Ejecuta el worker de Celery y el scheduler Beat en terminales separadas**
    ```bash
    celery -A openlibrary worker --loglevel=info
    celery -A openlibrary beat --loglevel=info