"""WSGI config for bankautomat project."""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bankautomat.settings")

application = get_wsgi_application()
