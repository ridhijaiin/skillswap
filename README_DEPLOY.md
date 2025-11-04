Deployment notes

1) Install Python and Node on the target host.
2) Install dependencies: `pip install -r requirements.txt`.
3) Build tailwind assets: `python manage.py tailwind install` and `python manage.py tailwind build`.
4) Collect static: `python manage.py collectstatic --noinput`.
5) Use Gunicorn / Daphne behind a reverse proxy. Example Procfile provided.
6) For Docker: build with `docker build -t skillswap .` and run with appropriate environment variables (SECRET_KEY, DEBUG=0, DATABASE_URL, ALLOWED_HOSTS, etc.).

Notes:
- `requirements.txt` was generated from the current venv.
- `STATIC_ROOT` was set in settings so `collectstatic` can run.
