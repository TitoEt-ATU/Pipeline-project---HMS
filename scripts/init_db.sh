#!/usr/bin/env bash
# Helper script to (re)initialize the Postgres DB, create user/database, and apply migrations.
# Usage:
#  ./scripts/init_db.sh create   - create user and db if missing
#  ./scripts/init_db.sh migrate  - run flask db upgrade in app container
#  ./scripts/init_db.sh reset    - destroy data and recreate db and run migrations
#  ./scripts/init_db.sh all      - create and then migrate

set -euo pipefail
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT_DIR"

DB_CONTAINER_NAME="hms-postgres"
APP_SERVICE_NAME="app"
APP_CONTAINER_NAME="hms-app"

# Read variables from .env if present
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

DB_USER=${DB_USER:-hospital_user}
DB_PASSWORD=${DB_PASSWORD:-hospital_password}
DB_NAME=${DB_NAME:-hospital_management}
# Postgres superuser is whatever POSTGRES_USER is set in the container (often the initial DB user)
SUPERUSER=${POSTGRES_USER:-${DB_USER}}

function wait_for_db() {
  echo "Waiting for Postgres to be ready..."
  local i=0
  # Use the superuser to check if Postgres itself is ready by connecting to the postgres database
  while ! docker exec "$DB_CONTAINER_NAME" pg_isready -U "$SUPERUSER" -d postgres >/dev/null 2>&1; do
    sleep 1
    i=$((i+1))
    if [ $i -gt 60 ]; then
      echo "Timed out waiting for postgres to be ready"
      return 1
    fi
  done
  echo "Postgres is ready"
}

function create_user_and_db() {
  # Check for user
  if docker exec -i "$DB_CONTAINER_NAME" psql -U "$SUPERUSER" -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    echo "User $DB_USER already exists"
  else
    if [ "$SUPERUSER" = "$DB_USER" ]; then
      echo "(Running as superuser $SUPERUSER) No need to create $DB_USER — it's the initial superuser."
    else
      echo "Creating user $DB_USER"
      docker exec -i "$DB_CONTAINER_NAME" psql -U "$SUPERUSER" -d postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
    fi
  fi

  # Check for DB
  if docker exec -i "$DB_CONTAINER_NAME" psql -U "$SUPERUSER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1; then
    echo "Database $DB_NAME already exists"
  else
    echo "Creating database $DB_NAME owned by $DB_USER"
    docker exec -i "$DB_CONTAINER_NAME" psql -U "$SUPERUSER" -d postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"
  fi

  # Grant privileges
  docker exec -i "$DB_CONTAINER_NAME" psql -U "$SUPERUSER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
  echo "User and database creation complete"
}

function run_migrations() {
  # Ensure app container is running
  if ! docker ps --format '{{.Names}}' | grep -q "$APP_CONTAINER_NAME"; then
    echo "App container not running: starting app container (service: $APP_SERVICE_NAME)"
    docker-compose up -d $APP_SERVICE_NAME
    sleep 3
  fi

  echo "Running migrations in $APP_CONTAINER_NAME"
  # Run flask db upgrade inside app container, ensure environment variables are set
  docker exec -i "$APP_CONTAINER_NAME" bash -lc "export FLASK_APP=src.app:create_app && flask db upgrade"
  echo "Migrations applied"
}

function reset_db() {
  echo "Stopping containers and removing volumes..."
  docker-compose down -v
  echo "Bringing up db and app containers"
  docker-compose up -d db
  # Wait for db
  wait_for_db
  create_user_and_db
  docker-compose up -d $APP_SERVICE_NAME
  sleep 3
  run_migrations
}

case ${1:-"all"} in
  create)
    docker-compose up -d db
    wait_for_db
    create_user_and_db
    ;;
  migrate)
    run_migrations
    ;;
  reset)
    reset_db
    ;;
  all)
    docker-compose up -d db
    wait_for_db
    create_user_and_db
    docker-compose up -d $APP_SERVICE_NAME
    sleep 3
    run_migrations
    ;;
  *)
    echo "Usage: $0 {create|migrate|reset|all}"
    exit 1
    ;;
esac

exit 0
