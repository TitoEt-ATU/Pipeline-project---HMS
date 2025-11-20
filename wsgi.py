from src.app import create_app
from ddtrace import patch_all

# Expose the WSGI application for gunicorn / uWSGI
application = create_app()
patch_all()