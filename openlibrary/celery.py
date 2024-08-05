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

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from django_celery_beat.models import PeriodicTask, IntervalSchedule

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.DAYS,
    )
    PeriodicTask.objects.get_or_create(
        interval=schedule,
        name='Fetch books from OpenLibrary daily',
        task='books.tasks.fetch_books_from_openlibrary',
    )