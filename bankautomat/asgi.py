"""ASGI config for bankautomat project."""

import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bankautomat.settings")

application = get_asgi_application()
