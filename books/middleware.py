# books/middleware.py

import logging
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        logger.error(f"Exception occurred: {exception}", exc_info=True)
        return render(request, 'error.html', status=500)
