# Dockerfile
FROM python:3.12.6

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Gunicorn+Uvicorn for prod
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app:app", \
     "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "60"]