FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier la structure des fichiers selon l'organisation réelle
COPY src/app.py /app/
COPY src/model.py /app/
COPY src/train.py /app/
COPY src/types_custom.py /app/
COPY src/utils.py /app/

# Copier les dossiers de données et modèles
COPY src/data/ /app/data/
COPY src/model/ /app/model/

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' fiestappuser && \
    chown -R fiestappuser:fiestappuser /app
USER fiestappuser

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]