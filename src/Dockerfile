# Dockerfile
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . /app/

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' fiestappuser && \
    chown -R fiestappuser:fiestappuser /app
USER fiestappuser

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
