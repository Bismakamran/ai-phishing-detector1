# Use lightweight Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose a default port for local dev; Railway provides $PORT at runtime
EXPOSE 8000

# Health check (uses $PORT provided by platform)
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD bash -lc 'curl -fsS http://localhost:${PORT:-8000}/health || exit 1'

# Run the application (bind to $PORT if provided)
CMD ["bash","-lc","exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120 app:app"]
