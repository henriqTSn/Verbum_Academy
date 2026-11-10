FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variáveis de ambiente devem vir de GitHub Secrets ou do ambiente de execução
# Nunca versionar chaves reais
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

EXPOSE 8000

RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
