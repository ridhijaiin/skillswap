SkillSwap

A small Django-based marketplace for skills and courses. This repository contains the project sources, a `requirements.txt` generated from the current virtualenv, and basic deployment instructions in `README_DEPLOY.md`.

Quick start (development):

1. Create and activate a Python virtual environment.
2. Install requirements:

   pip install -r requirements.txt

3. Run migrations:

   python manage.py migrate

4. Create a superuser (optional):

   python manage.py createsuperuser

5. Run the dev server:

   python manage.py runserver

Notes:
- Tailwind is configured via the `theme` app. To build Tailwind assets run:

   python manage.py tailwind install
   python manage.py tailwind build

- For deployment see `README_DEPLOY.md` for a simple Docker/Gunicorn example.
