# Pipeline-project---HMS
Hospital Management System

Run locally with Datadog tracing
--------------------------------
To run the Flask application locally with Datadog automatic tracing and profiling:

1) Activate your Python environment
```bash
source venv/bin/activate
```

2) Ensure dependencies are installed
```bash
pip install -r requirements.txt
```

3) Start a local Datadog agent (optional; recommended for APM/profiler)
```bash
docker-compose up -d datadog
```

4) Run the app with ddtrace-run using the package/module form so python resolves `src.*` imports
```bash
# from repo root
DD_SERVICE="hms-app" DD_ENV="dev" ddtrace-run python -m src.app
```

You can also use the helper script:
```bash
chmod +x scripts/run_dev.sh
./scripts/run_dev.sh
```

Notes:
- The application lives under `src/` and uses package relative imports; launching `python app.py` from the repository root will fail because there's no top-level `app.py`.
- If you want reliable local tracing & profiling, ensure the Datadog agent is running and `DD_AGENT_HOST` is configured to point to it.
- If ddtrace or the Datadog agent do not support your local Python version, use Python 3.11 (the CI uses 3.11).

DB init and migrations
-----------------------
I included `scripts/init_db.sh` to manage the Postgres DB and migrations.

Examples:
```bash
# Create user & DB and apply migrations (uses docker-compose container names)
./scripts/init_db.sh create
./scripts/init_db.sh migrate

# All-in-one (create DB/user, start containers, then run migrations)
./scripts/init_db.sh all

# Reset DB (this destroys data by removing volumes) and re-initialize
./scripts/init_db.sh reset
```
