FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Valores que não parecem segredos reais
ENV DJANGO_SECRET_KEY=dev-secret-key-change-me
ENV VERBUM_ENCRYPTION_KEY=dev-encryption-key-change-me
ENV DEBUG=True
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
