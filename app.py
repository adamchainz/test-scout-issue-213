import html
import os
import sys

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path
from django.utils.crypto import get_random_string

settings.configure(
    DEBUG=(os.environ.get("DEBUG", "") == "1"),
    ALLOWED_HOSTS=["*"],  # Disable host header validation
    ROOT_URLCONF=__name__,  # Make this module the urlconf
    SECRET_KEY=get_random_string(50),  # We aren't using any security features but Django requires this setting
    INSTALLED_APPS=[
        'scout_apm.django',
    ],
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
