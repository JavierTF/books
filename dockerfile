# Usa una imagen base de Python
FROM python:3.9

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y los instala
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto
COPY . /app/

# Expone el puerto en el que Django correrá
EXPOSE 8000

# Ejecuta el servidor de desarrollo de Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "openlibrary.wsgi:application"]
