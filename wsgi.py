from src.app import create_app

# Expose the WSGI application for gunicorn / uWSGI
application = create_app()
