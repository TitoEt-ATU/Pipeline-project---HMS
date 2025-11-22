FROM python:3.11-slim

# Prevents Python from writing .pyc files to disc and ensures stdout/stderr are not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps needed for some python packages (if any). Keep minimal for slim image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python deps. We add gunicorn to run the app in container.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . /app

# Ensure instance folder exists (Flask may expect instance/ to be present)
RUN mkdir -p /app/instance

EXPOSE 5000

# Use the WSGI entrypoint we provide (wsgi.application)
ENV FLASK_APP=src.app:create_app

# Run with gunicorn; using 2 workers as a reasonable default for a small container.
# We point gunicorn at the `wsgi` module which constructs the app via create_app().

RUN pip install ddtrace
CMD ["ddtrace-run", "gunicorn", "wsgi:application", "-b", "0.0.0.0:5001", "--workers", "2"]
