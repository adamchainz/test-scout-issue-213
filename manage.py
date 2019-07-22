import html
import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from django.utils.crypto import get_random_string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings.configure(
    # Django core
    ALLOWED_HOSTS=["*"],  # Disable host header validation
    BASE_DIR=BASE_DIR,
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    INSTALLED_APPS=[
        'django.contrib.staticfiles',
        'compressor',
        'scout_apm.django',
    ],
    LOGGING={
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'stdout': {
                'format': '%(asctime)s %(levelname)s %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%z',
            },
        },
        'handlers': {
            'stdout': {
                'class': 'logging.StreamHandler',
                'formatter': 'stdout',
            },
            'scout_apm': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'scout_apm_debug.log',
            },
        },
        'root': {
            'handlers': ['stdout'],
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
        },
        'loggers': {
            # as per https://docs.scoutapm.com/#django-logging
            'scout_apm': {
                'handlers': ['scout_apm'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    },
    ROOT_URLCONF=__name__,  # Make this module the urlconf
    SECRET_KEY=get_random_string(50),  # We aren't using any security features but Django requires this setting
    # django.contrib.staticfiles
    STATICFILES_FINDERS=[
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    ],
    STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles'),
    STATIC_URL='/static/',
    # scout_apm
    SCOUT_MONITOR=True,
    SCOUT_KEY=os.environ['SCOUT_KEY'],
    SCOUT_NAME="Test App",
)


def index(request):
    name = request.GET.get("name", "World")
    return HttpResponse(f"Hello, {html.escape(name)}!")


urlpatterns = [
    path("", index),
]

app = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
