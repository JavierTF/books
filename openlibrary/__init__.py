from __future__ import absolute_import, unicode_literals

# Esto asegura que las tareas de Celery se carguen cuando Django se inicie.
from .celery import app as celery_app

__all__ = ('celery_app',)