FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

# Collect static
ENV DJANGO_SETTINGS_MODULE=skillswap.settings
RUN python manage.py collectstatic --noinput || true

# Expose port and run
EXPOSE 8000
CMD ["gunicorn", "skillswap.wsgi:application", "--bind", "0.0.0.0:8000"]
