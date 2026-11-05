FROM python:3.12-slim

WORKDIR /app

# Cria usuário não-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appuser /app

# Valores padrão apenas para desenvolvimento/CI (não são segredos reais)
ENV DJANGO_SECRET_KEY=dev-secret-key-change-me
ENV VERBUM_ENCRYPTION_KEY=dev-encryption-key-change-me
ENV DEBUG=True
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

USER appuser

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
