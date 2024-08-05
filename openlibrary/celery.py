from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece el módulo de configuración predeterminado de Django para 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openlibrary.settings')

app = Celery('openlibrary')

# Carga la configuración de Celery desde Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carga tareas de todos los módulos de tareas registradas en Django apps
app.autodiscover_tasks()