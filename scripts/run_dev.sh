#!/usr/bin/env bash
# Dev run helper to start the Flask app with Datadog auto-instrumentation.
# Usage: ./scripts/run_dev.sh [--no-agent]
set -euo pipefail

# Default environment variables for Datadog
export DD_SERVICE=${DD_SERVICE:-hms-app}
export DD_ENV=${DD_ENV:-dev}
export DD_LOGS_INJECTION=${DD_LOGS_INJECTION:-true}
export DD_PROFILING_ENABLED=${DD_PROFILING_ENABLED:-true}
export DD_DATA_STREAMS_ENABLED=${DD_DATA_STREAMS_ENABLED:-true}
export DD_TRACE_REMOVE_INTEGRATION_SERVICE_NAMES_ENABLED=${DD_TRACE_REMOVE_INTEGRATION_SERVICE_NAMES_ENABLED:-true}
export DD_APPSEC_ENABLED=${DD_APPSEC_ENABLED:-false}
export DD_IAST_ENABLED=${DD_IAST_ENABLED:-false}
export DD_APPSEC_SCA_ENABLED=${DD_APPSEC_SCA_ENABLED:-false}
# Optional: set DD_AGENT_HOST to the datadog agent address if using docker-compose
export DD_AGENT_HOST=${DD_AGENT_HOST:-localhost}

# Useful DEBUG env for ddtrace itself
export DD_TRACE_DEBUG=${DD_TRACE_DEBUG:-false}

# Activate venv if present
if [ -d "venv" ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi

# If --no-agent passed, we don't try to run docker agent. Otherwise suggest running compose.
if [ "${1:-}" != "--no-agent" ]; then
  if ! docker ps --format '{{.Names}}' | grep -q datadog-agent; then
    echo "Datadog agent not found running locally. You can run: docker-compose up -d datadog"
  fi
fi

# Run the app as a module so package imports resolve: src.app
# ddtrace-run wrapper is used to enable Datadog autoinstrumentation.
# This assumes ddtrace is installed in the active venv.
if command -v ddtrace-run >/dev/null 2>&1; then
  echo "Starting app with ddtrace..."
  ddtrace-run python -m src.app
else
  echo "ddtrace-run not found. Installing into venv (pip install ddtrace) and running without ddtrace..."
  python -m pip install --upgrade pip setuptools wheel
  python -m pip install ddtrace
  python -m src.app
fi
