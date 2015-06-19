"""
WSGI config for pipelion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/dotproj/djangostack-1.7.8-0/apps/django/django_projects/pipelion')
os.environ.setdefault("PYTHON_EGG_CACHE",
                      '/home/dotproj/djangostack-1.7.8-0/apps/django/django_projects/pipelion/egg_cache')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pipelion.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
